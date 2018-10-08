# -*- coding: utf-8 -*-
import six
from copy import deepcopy

from .utils import classproperty
from .fields import BxField
from . import settings as bx_settings, token_storage as default_storage
from .repository import BaseBxRepository, BxEntityQuery
from .adapter import BaseBxAdapter


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
        'create_action': 'add',
        'default_prefix': ''
    }
    repository = None

    def __new__(mcs, name, bases, attrs):
        to_pop = {}
        for k in attrs:
            if issubclass(type(attrs[k]), BxField):
                to_pop.update({k: attrs[k]})
        for k in to_pop:
            attrs.pop(k)
        attrs.update({'to_instance_dict': to_pop})
        instance_bx_meta = deepcopy(mcs._bx_meta)
        instance_bx_meta.update(attrs.get('_bx_meta', {}))
        domain = instance_bx_meta['domain']
        attrs['to_instance_dict'].update({'_bx_meta': instance_bx_meta})
        if '_bx_meta' in attrs:
            attrs.pop('_bx_meta')
        super_obj = super(BxEntityMeta, mcs).__new__(mcs, name, bases, attrs)
        super_obj.repository = instance_bx_meta['repository'](super_obj, instance_bx_meta, domain)
        return super_obj


class BxEntity(six.with_metaclass(BxEntityMeta)):
    def __init__(self, **kwargs):
        # type: (kwargs) -> None
        provided_id = kwargs.get('ID') or None
        if (issubclass(type(provided_id), BxField)):
            id_field = provided_id
        else:
            id_field = BxField('ID', provided_id, '')
        self._bx_meta = self.to_instance_dict['_bx_meta']
        self.to_instance_dict.update({'id': id_field})
        self.to_changed_fields = []
        for k in self.to_instance_dict:
            v = self.to_instance_dict[k]
            val_type = type(v)
            if issubclass(val_type, BxField):
                if v.bx_name in kwargs:
                    value = kwargs[v.bx_name]
                elif k in kwargs:
                    value = kwargs[k]
                    self.to_changed_fields.append(k)
                else:
                    value = v.value
                prefix = v.prefix if v.prefix is not None else self._bx_meta['default_prefix']
                new_v = val_type(v.bx_name, value, prefix)
                setattr(self, k, new_v)
        self.changed_fields = [] + self.to_changed_fields

    def __setattr__(self, key, value):
        if key != 'changed_fields' \
                and 'changed_fields' in self.__dict__ \
                and key in self.__dict__:
            field = getattr(self, key, None)
            if issubclass(type(field), BxField):
                field.validate_value(value)
                field.__set__(None, field.parse_value(value))
            if key not in self.changed_fields:
                self.changed_fields.append(key)
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
        self.changed_fields = []
        return self.id.value, created

    def delete(self):
        self.repository.delete(self)

    @classproperty
    def objects(cls):
        # type: () -> BxEntityQuery
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
            if issubclass(type(field), BxField):
                result.update(field.to_bitrix)
        else:
            for f in self.__dict__:
                field = getattr(self, f)
                if issubclass(type(field), BxField):
                    result.update(field.to_bitrix)
        return result

    @property
    def has_updates(self):
        return len(self.changed_fields) > 0
