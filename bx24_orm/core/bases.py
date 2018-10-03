# -*- coding: utf-8 -*-
import six

from .utils import classproperty
from .fields import BxField
from . import settings as bx_settings, token_storage as default_storage
from .repository import BaseBxRepository
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
