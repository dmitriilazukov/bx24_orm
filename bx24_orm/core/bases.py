# -*- coding: utf-8 -*-


import six

from .utils import classproperty
from .fields import BxField
from . import settings as bx_settings, token_storage as default_storage
from .bx_interface import (BxQueryBuilder, BxCallableMixin, BxQueryResponse, BxQuery, BxBatch, BxBatchCommand)
from .exceptions.code_exceptions import *
from .exceptions.bx_exceptions import *


class BaseBxAdapter(object):
    def __init__(self, entity_cls):
        self.entity_cls = entity_cls

    def from_bitrix(self, response):
        # type: (BxQueryResponse) -> BxEntity or list
        if response.result:
            if response.total > 1:
                return [self.entity_cls(**r) for r in response.result]
            else:
                return self.entity_cls(**response.result)
        else:
            return None

    @classmethod
    def to_bitrix(cls, bx_entity, force_all_fields=False):
        # type: (BxEntity, bool) -> dict
        return bx_entity.get_updates(force_all_fields)


class BaseBxRepository(object):
    GET, UPDATE, LIST, CREATE, DELETE = 'GET', 'UPDATE', 'LIST', 'CREATE', 'DELETE'
    actions = {GET: 'get_action',
               UPDATE: 'update_action',
               CREATE: 'create_action',
               LIST: 'list_action',
               DELETE: 'delete_action'}

    def __init__(self, entity_cls, domain=bx_settings.default_domain, token_storage=default_storage):
        # type: (BxEntity, str, object) -> None
        self.token_storage = token_storage
        self.domain = domain
        self.entity_cls = entity_cls
        self.adapter = entity_cls._bx_meta['adapter'](entity_cls)
        super(BaseBxRepository, self).__init__()

    def _build_query_name(self, action):
        entity_name = self.entity_cls._bx_meta['entity']
        action = self.entity_cls._bx_meta[self.actions[action]]
        if action:
            action = '.' + action
        return entity_name + action

    @property
    def token(self):
        return self.token_storage.get_token(self.domain)

    def get_by_id(self, entity_id):
        # type: (str or int) -> BxEntity
        """
        Searches for entity by provided id
        :param entity_id: entity id
        :return: entity
        """
        q = BxQuery(self._build_query_name(self.GET), {'ID': entity_id, 'auth': self.token}, self.domain)
        result = self._call(q)
        return self.adapter.from_bitrix(result)

    def update(self, entity):
        # type: (BxEntity) -> BxQueryResponse
        """
        Updates entity
        :param entity: entity to update
        :return: Bitrix response
        """
        params = self.adapter.to_bitrix(entity)
        params.update({'auth': self.token})
        q = BxQuery(self._build_query_name(self.UPDATE), params, self.domain)
        result = self._call(q)
        return result

    def create(self, entity):
        # type: (BxEntity) -> BxQueryResponse
        """
        Creates entity
        :param entity:  entity to create
        :return: Bitrix response
        """
        params = self.adapter.to_bitrix(entity, True)
        params.update({'auth': self.token})
        q = BxQuery(self._build_query_name(self.CREATE), params, self.domain)
        result = self._call(q)
        return result

    def delete(self, entity):
        q = BxQuery(self._build_query_name(self.DELETE), entity.id.to_bitrix, self.domain)
        result = self._call(q)
        return result

    def get_many(self, entity_ids):
        self._validate_before_many(entity_ids, (int, str, unicode))
        if len(entity_ids) > 50:
            raise NotImplementedError('Feature for fetching more than 50 items at time not realised')
        if len(entity_ids) == 0:
            return []
        queries = [BxBatchCommand(self._build_query_name(self.GET), {'ID': i}, 'id_{}'.format(i)) for i in entity_ids]
        q = BxBatch(queries, self.token, self.domain)
        q_result = self._call(q)
        return [self.adapter.from_bitrix(bx_response) for bx_response in q_result]

    def update_many(self, entity_list):
        # type: (list or tuple or set or frozenset) -> BxBatchResponse
        """
        Updates list of entitys in one batch
        :param entity_list: list of entitys to update
        :return: Bitrix response
        """
        self._validate_before_many(entity_list, self.entity_cls)
        queries = [BxBatchCommand(self._build_query_name(self.UPDATE), entity.get_updates())
                   for entity in entity_list if entity.has_updates]
        batch = BxBatch(queries, self.token, self.domain)
        result = self._call(batch)
        return result

    @property
    def objects(self):
        return BxEntityQuery(self.entity_cls, token_storage=self.token_storage, domain=self.domain)

    @staticmethod
    def _validate_before_many(target_list, target_type):
        if not type(target_type) in (set, frozenset, list, tuple):
            target_type = (target_type,)
        if type(target_list) not in (set, frozenset, list, tuple):
            raise ValueError('Expected iterable, got {}'.format(type(target_list)))
        if not all(type(i) in target_type for i in target_list):
            raise ValueError('List members must satisfy this types {}'.format(target_type))

    def _call(self, query, token_updated=False):
        # type: (BxQuery or BxBatch) -> BxQueryResponse
        try:
            result = query.call(1)
        except QueryLimitExceededException as e:
            raise e
        except InvalidTokenException as e:
            if not token_updated:
                query.parameters.update({'auth': self.token_storage.refresh_token(self.domain)})
                result = self._call(query, True)
            else:
                raise e
        except NotFoundException as e:
            raise EntityNotFoundException(e.error, e.error_description)
        except Exception:
            raise
        return result


class BxEntityMeta(type):
    _bx_meta = {
        'repository': BaseBxRepository,
        'adapter': BaseBxAdapter,
        'domain': bx_settings.default_domain,
        'transport': bx_settings.default_transport,
        'get_action': 'get',
        'delete_action': 'delete',
        'list_action': 'list',
        'update_action': 'update',
        'create_action': 'add'
    }
    repository = None

    def __new__(mcs, name, bases, attrs):
        to_pop = {}
        for k in attrs:
            if isinstance(attrs[k], BxField):
                to_pop.update({k: attrs[k]})
        for k in to_pop:
            attrs.pop(k)
        attrs.update({'to_instance_dict': to_pop})
        if '_bx_meta' in attrs:
            attrs['_bx_meta'].update(mcs._bx_meta)
        else:
            attrs.update({'_bx_meta': mcs._bx_meta})
        mcs._bx_meta = attrs['_bx_meta']
        domain = mcs._bx_meta['domain']
        super_obj = super(BxEntityMeta, mcs).__new__(mcs, name, bases, attrs)
        super_obj.repository = mcs._bx_meta['repository'](super_obj, domain)
        return super_obj


class BxEntity(six.with_metaclass(BxEntityMeta)):
    def __init__(self, **kwargs):
        # type: (kwargs) -> None
        provided_id = kwargs.get('id') or kwargs.get('ID') or None
        id_field = provided_id if isinstance(provided_id, BxField) else BxField('ID',
                                                                                value=provided_id,
                                                                                prefix="")
        self.to_instance_dict.update({'id': id_field})
        for k in self.to_instance_dict:
            v = self.to_instance_dict[k]
            if isinstance(v, BxField):
                value = kwargs[v.bx_name] if v.bx_name in kwargs else v.value
                new_v = BxField(v.bx_name, value, v.prefix)
                setattr(self, k, new_v)
        self.changed_fields = []

    def __setattr__(self, key, value):
        if key != 'changed_fields' \
                and 'changed_fields' in self.__dict__ \
                and key in self.__dict__ \
                and key not in self.changed_fields:
            self.changed_fields.append(key)
        field = getattr(self, key, None)
        if type(field) == BxField:
            BxField.__set__(field, None, value)
        else:
            self.__dict__.update({key: value})

    @classmethod
    def get(cls, entity_id):
        return cls.repository.get_by_id(entity_id)

    @classmethod
    def get_many(cls, entity_ids):
        return cls.repository.get_many(entity_ids)

    def save(self):
        if self.id.value:
            result = self.repository.update(self)
            created = result.result
        else:
            result = self.repository.create(self)
            self.id = result.result
            created = True
        return self.id.value, created

    def delete(self):
        self.repository.delete(self)

    @classproperty
    def objects(cls):
        return cls.repository.objects

    def get_updates(self, force_all_fields=False):
        result = {}
        if self.has_updates and not force_all_fields:
            entity_id = getattr(self, 'id')
            if not isinstance(entity_id, BxField):
                raise ValueError('id field should have BxField type')
            if entity_id.value:
                result.update(entity_id.to_bitrix)
        for f in self.changed_fields:
            field = getattr(self, f)
            if type(field) is BxField:
                result.update(field.to_bitrix)
        else:
            for f in self.__dict__:
                field = getattr(self, f)
                if isinstance(field, BxField):
                    result.update(field.to_bitrix)
        return result

    @property
    def has_updates(self):
        return len(self.changed_fields) > 0


class BxEntityQuery(BxQueryBuilder, BxCallableMixin):
    def __init__(self,
                 target_entity_cls,
                 token_storage=default_storage,
                 domain=bx_settings.default_domain,
                 transport=bx_settings.default_transport):
        # type: (BxEntity, object, str, str) -> None
        self.entity_cls = target_entity_cls
        self.token_storage = token_storage
        self.adapter = target_entity_cls._bx_meta['adapter'](target_entity_cls)
        self.domain = domain
        self.transport = transport
        action = '.' + self.entity_cls._bx_meta['list_action'] if self.entity_cls._bx_meta.get('list_action') else ''
        self.url = 'https://{d}.bitrix24.ru/rest/{e}{a}.{t}'.format(d=domain,
                                                                    e=target_entity_cls._bx_meta['entity'],
                                                                    a=action,
                                                                    t=transport)
        super(BxEntityQuery, self).__init__()

    @property
    def token(self):
        return self.token_storage.get_token(self.domain)

    def __iter__(self):
        return iter(self.all())

    def resolve_field_name(self, option):
        if option in self.entity_cls.to_instance_dict:
            return self.entity_cls.to_instance_dict[option].bx_name
        else:
            return option

    def call(self, max_retries=0):
        max_retries -= 1
        try:
            params = dict(self.build(), auth=self.token)
            result = self._call(self.url, params)
        except QueryLimitExceededException:
            if max_retries >= 0:
                result = self.call(max_retries)
            else:
                raise
        return BxQueryResponse(result)

    def all(self):
        return self.adapter.from_bitrix(self.call())
