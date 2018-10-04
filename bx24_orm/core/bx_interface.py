# -*- coding: utf-8 -*-

import requests
import time
import uuid
from itertools import chain

from six.moves import urllib
from .exceptions import code_exceptions as ce


class BxQueryBuilder(object):
    query_options = {'gte': '>=', 'gt': '>', 'lte': '<=', 'lt': '<', 'contains': '%', 'in': ''}

    def __init__(self):
        self._filter = {}
        self._select = set()
        self._order = {}
        super(BxQueryBuilder, self).__init__()

    def resolve_field_name(self, option):
        return option

    def filter(self, **kwargs):
        if len(kwargs) == 0:
            return self
        for k in kwargs:
            v = kwargs[k]
            options = k.lower().split('__')
            options[0] = self.resolve_field_name(options[0])
            if len(options) > 2:
                raise ValueError('Invalid query: {}'.format(k))
            if options[0] in self.query_options:
                raise ValueError('Filter command should start with target field name. Found: {}'.format(options[0]))
            if len(options) == 1:
                formatted_key = 'FILTER[{}]'.format(str(options[0]).upper())
                self._filter.update({formatted_key: v})
            else:
                if options[1] not in self.query_options:
                    raise ValueError('Unexpected query option. Got {}. Expected {}'.format(options[1],
                                                                                           self.query_options.keys()))
                if options[1] == 'in':
                    if type(v) not in (set, frozenset, tuple, list):
                        raise ValueError('Expected list type. Got {}'.format(type(v)))
                    for i, val in enumerate(v):
                        formatted_key = 'FILTER[{}][{}]'.format(options[0].upper(), i)
                        self._filter.update({formatted_key: val})
                else:
                    formatted_key = 'FILTER[{}{}]'.format(self.query_options[options[1]], str(options[0]).upper())
                    self._filter.update({formatted_key: v})
        return self

    def select(self, *args):
        for a in args:
            a = self.resolve_field_name(str(a).lower())
            self._select.update((str(a).upper(),))
        return self

    def build(self):
        params = {}
        params.update(self._filter)
        for k in self._order:
            v = self._order[k]
            params.update({'ORDER[{}]'.format(k): v})
        for i, v in enumerate(self._select):
            params.update({'SELECT[{}]'.format(i): v})
        return params

    def order(self, *args):
        for a in args:
            a = self.resolve_field_name(str(a).lower())
            a = str(a).upper()
            if a.startswith('-'):
                self._order.update({a[1:]: 'DESC'})
            else:
                self._order.update({a: 'ASC'})
        return self


class BxResponse(object):
    def __init__(self):
        pass

    def __parse_raw_result(self, raw_result):
        pass


class BxQueryResponse(BxResponse):
    def __init__(self, raw_result):
        # type: (dict) -> None
        """
        Represents bitrix response
        :param raw_result: response from bitrix as dict(json)
        """
        super(BxQueryResponse, self).__init__()
        self.__parse_raw_result(raw_result)

    def __parse_raw_result(self, raw_result):
        # type: (dict) -> None
        self.result = raw_result.get('result')
        self.error = raw_result.get('error')
        self.result_next = raw_result.get('next') or 0
        self.total = raw_result.get('total') or 1 if self.result else 0


class BxBatchResponse(BxResponse):
    def __init__(self, raw_result):
        # type: (dict) -> None
        """
        Represents batch response
        :param raw_result: response from bitrix batch as dict(json)
        """
        super(BxBatchResponse, self).__init__()
        self.__parse_raw_result(raw_result)

    def __parse_raw_result(self, raw_result):
        # type: (dict) -> None
        self.result, self.error, self.result_next, self.result_total = {}, {}, {}, {}
        self.keys = []
        if 'result' in raw_result:
            self.result = raw_result['result'].get('result') or {}
            self.error = raw_result['result'].get('result_error') or {}
            self.result_next = raw_result['result'].get('result_next') or {}
            self.result_total = raw_result['result'].get('result_total') or {}
            self.keys = chain(self.result, self.error)
        else:
            self.error = raw_result['error']

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        for k in self.keys:
            return self.__getitem__(k)
        raise StopIteration

    @property
    def cmd_names(self):
        return self.keys[:]

    def __getitem__(self, item):
        # type: (str) -> BxQueryResponse
        """
        Gets batch`s result by cmd name
        :param item: cmd name
        """
        return BxQueryResponse({'result': self.result.get(item),
                                'error': self.error.get(item),
                                'next': self.result_next.get(item) or 0,
                                'total': self.result_total.get(item)} or 0)


class BxCallableMixin(object):
    _http_code_to_exception = {
        400: ce.NotFoundException,
        401: ce.TokenExpiredException,
        403: ce.TokenNotFoundException,
        404: ce.InvalidQueryException
    }

    def __init__(self):
        super(BxCallableMixin, self).__init__()

    def call(self, max_retries):
        pass

    def safe_call(self):
        pass

    def _call(self, request_url, data):
        # type: () -> dict
        """
        Performs request, if error occured throws exception
        :return: raw result of request as dict
        """
        exception_info = {'error': '', 'error_description': ''}
        try:
            response = requests.post(request_url, data=data)
            result = response.json()
        except ValueError:
            exception_info['error'] = ce.NOT_JSON_RESPONSE
            exception_info['error_description'] = response.text
            raise ce.NotJsonResponseException(**exception_info)
        except requests.ConnectionError as e:
            exception_info['error'] = ce.NETWORK_ERROR
            exception_info['error_description'] = 'Request failed due network error: {}'.format(str(e))
            raise ce.RequestFailedException(**exception_info)
        if 200 <= response.status_code < 300:
            result = result
        if 300 <= response.status_code < 400:
            exception_info['error'] = ce.UNEXPECTED_HTTP_CODE
            exception_info['error_description'] = response.text
            raise ce.UnexpectedResponseCodeException(**exception_info)
        elif response.status_code in (400, 401, 403, 404):
            exception_info.update(result)
            status_code = response.status_code
            if exception_info['error'] == ce.NO_AUTH_FOUND:
                status_code = 403
            raise self._http_code_to_exception[status_code](**exception_info)
        elif 400 <= response.status_code < 500:
            exception_info['error'] = 'Failed with status code {}'.format(response.status_code)
            exception_info['error_description'] = response.text
            raise ce.InvalidRequestException(**exception_info)
        elif response.status_code >= 500:
            exception_info = result
            if exception_info['error'] == ce.QUERY_LIMIT_EXCEEDED:
                raise ce.QueryLimitExceededException(**exception_info)
            else:
                raise ce.RequestFailedException(**exception_info)
        return result


class BxBatchCommand(object):
    @staticmethod
    def __encoded_dict(in_dict):
        # type: (dict) -> dict
        """
        Returns encoded dict to escape utf-8 urllib issues
        :param in_dict: dict to encode
        :return: dict with all strings in ascii
        """
        out_dict = {}
        for k in in_dict:
            v = in_dict[k]
            if isinstance(v, unicode):
                v = v.encode('utf8')
            elif isinstance(v, str):
                # Must be encoded in UTF-8
                v.decode('utf8')
            out_dict[k] = v
        return out_dict

    def __init__(self, query, parameters, name=None):
        # type: (str, dict, str) -> None
        """
        Container for batch commands
        :param query: query like crm.deal.get and etc.
        :param parameters: query parameters
        :param name: cmd[{{name}}]
        """
        self.name = name
        self.query = query
        self.parameters = parameters

    def as_batch(self):
        # type: () -> dict
        """
        Creates batch string
        :return: dict, like { cmd[cmd_name]: url_with_params }
        """
        cmd_name = self.name if self.name else str(uuid.uuid4())[:4]
        urlencode = urllib.parse.urlencode
        return {'cmd[{}]'.format(cmd_name): '{u}?{p}'.format(u=self.query,
                                                             p=urlencode(self.__encoded_dict(self.parameters)))}


class BxQuery(BxBatchCommand, BxCallableMixin):
    def __init__(self, query, params, domain, transport='json', cmd_name=None):
        # type: (str, dict, str, str, str) -> None
        """
        Performs request to bitrix
        :param query: query like crm.deal.get or other
        :param params: query parameters
        :param domain: third level bitrix domain
        :param transport: response format
        :param cmd_name: (optional) specify to prevent getting random name in as_batch method
        """
        if transport == 'xml':
            raise NotImplementedError('Xml transport feature not implemented')
        super(BxQuery, self).__init__(query, params, cmd_name)
        self.transport = transport
        self.request_url = 'https://{}.bitrix24.ru/rest/{}.{}/'.format(domain, query, transport)

    def call(self, max_retries=0):
        # type: (int) -> BxQueryResponse
        """
        Performs request to bitrix with opportunity to repeat request if query limit exceeded
        :param max_retries: number of retries before give up in case of QUERY_LIMIT_EXCEEDED Exception
        :return: result of query
        """
        max_retries -= 1
        try:
            raw_result = self._call(self.request_url, self.parameters)
            result = BxQueryResponse(raw_result)
        except ce.QueryLimitExceededException:
            if max_retries >= 0:
                time.sleep(2)
                result = self.call(max_retries)
            else:
                raise
        return result

    def safe_call(self):
        # type: () -> BxQueryResponse
        """
        Same as call, but instead of raising exception send it in result
        :return: BxResponse object
        """
        try:
            return self.call(max_retries=1)
        except ce.BxException as e:
            error = {'error': e.error, 'error_description': e.error_description}
        except Exception:
            raise
        return BxQueryResponse({'error': error})


class BxBatch(BxCallableMixin):
    def __init__(self, commands, token, domain, halt=0, transport='json'):
        # type: (list, str, str, int, str) -> None
        """
        Creates bitrix batch request object
        :param commands: iterable of BxBatchCommand objects
        :param token: access token
        :param halt: terminate batch if one of commands failed
        :param domain: portal`s third level domain
        :param transport: response format
        """
        super(BxBatch, self).__init__()
        if transport == 'xml':
            raise NotImplementedError('Xml transport feature not implemented')
        self.request_url = 'https://{}.bitrix24.ru/rest/batch.{}/'.format(domain, transport)
        self.parameters = {'halt': halt, 'auth': token}
        self.commands = {}
        for c in commands:
            if not isinstance(c, BxBatchCommand):
                raise ValueError('Command {} type is not <BxBatchCommand>'.format(c))
            self.commands.update(c.as_batch())

    def call(self, max_retries=0):
        # type: (int) -> BxBatchResponse
        """
        Performs batch call
        :param max_retries: Number of tries before give in in case of QUERY_LIMIT_EXCEEDED exception
        :return:
        """
        max_retries -= 1
        try:
            data = dict(self.parameters, **self.commands)
            result = BxBatchResponse(self._call(self.request_url, data))
        except ce.QueryLimitExceededException:
            if max_retries >= 0:
                time.sleep(2)
                result = self.call(max_retries)
            else:
                raise
        return result

    def safe_call(self):
        # type: () -> BxBatchResponse
        """
        Same as call, but instead of raising exception send it in result
        :return: BxBatchResponse object
        """
        try:
            result = self.call(max_retries=1)
        except ce.BxException as e:
            result = BxBatchResponse({'error': {'error': e.error, 'error_description': e.error_description}})
        except Exception:
            raise
        return result
