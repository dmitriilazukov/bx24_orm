# -*- coding: utf-8 -*-
from bx24_orm.core import settings, token_storage
from bx24_orm.core.bx_interface import (BxQuery, BxBatch, BxBatchCommand, BxQueryBuilder, BxCallableMixin, BxQueryResponse)
from .exceptions.code_exceptions import *
from .exceptions.bx_exceptions import *




class BaseBxRepository(object):
    GET, UPDATE, LIST, CREATE, DELETE = 'GET', 'UPDATE', 'LIST', 'CREATE', 'DELETE'
    REPOSITORY_ACTIONS = {
        GET: 'get_action',
        UPDATE: 'update_action',
        CREATE: 'create_action',
        LIST: 'list_action',
        DELETE: 'delete_action'
    }
    actions = REPOSITORY_ACTIONS

    def __init__(self, entity_cls, domain=settings.default_domain, token_storage=token_storage):
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


class BxEntityQuery(BxQueryBuilder, BxCallableMixin):
    def __init__(self,
                 target_entity_cls,
                 token_storage=token_storage,
                 domain=settings.default_domain,
                 transport=settings.default_transport):
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
