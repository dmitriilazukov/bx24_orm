# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime
from dateutil.parser import parse
import six


class BxField(object):
    def __init__(self, bx_name, value=None, prefix=None):
        # type: (six.string_types, object, six.string_types) -> None
        """
        Represents bitrix field
        :param bx_name: name on bitrix portal like UF_CRM_XXXXXX
        :param value: initial value
        :param prefix: prefix before parameters dict, e.g FIELD in ORM module
        """
        self._value = value
        self._bx_name = bx_name.upper()
        self._prefix = prefix.upper() if issubclass(type(prefix), six.string_types) else None
        super(BxField, self).__init__()

    def parse_value(self, value):
        return value

    @property
    def prefix(self):
        return self._prefix

    @property
    def bx_name(self):
        return self._bx_name

    @property
    def value(self):
        # type: () -> object
        """
        Returns copy of contained value to prevent untracked changes
        :return: value
        """
        return deepcopy(self._value)

    def __set__(self, instance, value):
        self._value = value

    @staticmethod
    def __format_value(key, value):
        # type: (str, object or list or tuple or set or frozenset) -> dict
        """
        Recursively unwrap field to properly formed dict of params
        :param key: current key
        :param value: value to unwrap
        :return: dict of parameters
        """
        result = {}
        if type(value) in (list, tuple, set, frozenset):
            for i, v in enumerate(value):
                result.update(BxField.__format_value(key + '[{}]'.format(i), v))
        elif type(value) is dict:
            for k in value:
                v = value[k]
                result.update(BxField.__format_value(key + '[{}]'.format(k.upper()), v))
        elif value is not None:
            result.update({key: value})
        return result

    def validate_value(self, value):
        return True

    def __call__(self, *args, **kwargs):
        return deepcopy(self._value)

    def __str__(self):
        return self._value.__str__()

    @property
    def to_bitrix(self):
        # type: () -> dict
        """
        Converts field into valid parameter or parameters to bitrix
        :return: Dict representing bitrix parameter
        """
        if self._prefix:
            key = '{}[{}]'.format(self._prefix, self._bx_name)
        else:
            key = '{}'.format(self._bx_name)
        return self.__format_value(key, self.value)


class BxDateTime(BxField):

    def __init__(self, bx_name, value=None, prefix=None):
        try:
            self.validate_value(value)
            value = self.parse_value(value)
        except ValueError as err:
            raise err
        super(BxDateTime, self).__init__(bx_name, value, prefix)

    def parse_value(self, value):
        if not value:
            return None
        if type(value) == datetime:
            return value
        else:
            return parse(value)

    def validate_value(self, value):
        if isinstance(value, datetime):
            return True
        if value is None:
            return None
        if issubclass(type(value), six.string_types):
            if value.strip() == '':
                return None
            else:
                try:
                    parse(value)
                    return True
                except ValueError as err:
                    raise err
        raise ValueError('Datetime or str instance expected. Got {}'.format(type(value)))

    @property
    def to_bitrix(self):
        if self._prefix:
            key = '{}[{}]'.format(self._prefix, self._bx_name)
        else:
            key = '{}'.format(self._bx_name)
        if self._value:
            try:
                v = self._value.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')
            except ValueError:
                v = self._value.strftime('%Y-%m-%dT%H:%M:%S.%f')
        else:
            v = ''
        return {key: v}


class BxBoolean(BxField):
    def __init__(self, bx_name, value=None, prefix=None):
        if self.validate_value(value):
            value = self.parse_value(value)
            super(BxBoolean, self).__init__(bx_name, value, prefix)
        else:
            raise RuntimeError('Failed to initialize BxBoolean with value = {}'.format(value))

    def parse_value(self, value):
        if value is None:
            return False
        if issubclass(type(value), six.string_types) and value.upper().strip() in ('Y', 'N'):
            return True if value.upper().strip() is 'Y' else False
        if type(value) is bool:
            return value
        raise ValueError('Expected Y/N or bool or None. Got {}'.format(type(value)))

    def validate_value(self, value):
        if value is None:
            return True
        if issubclass(type(value), six.string_types) and value.upper().strip() in ('Y', 'N'):
            return True
        if type(value) is bool:
            return True
        raise ValueError('Expected Y/N or bool or None. Got {}'.format(type(value)))

    @property
    def to_bitrix(self):
        if self._prefix:
            key = '{}[{}]'.format(self._prefix, self._bx_name)
        else:
            key = '{}'.format(self._bx_name)
        v = 'Y' if self._value else 'N'
        return {key: v}
