# -*- coding: utf-8 -*-


from bx24_orm.core.bases import BxEntity
from bx24_orm.core.fields import BxField, BxDateTime


class BaseLead(BxEntity):
    _bx_meta = {
        'entity': 'crm.lead'
    }


class BaseDeal(BxEntity):
    title = BxField('TITLE', prefix='FIELDS')
    type_id = BxField('TYPE_ID', prefix='FIELDS')
    stage = BxField('STAGE_ID', prefix='FIELDS')
    opportunity = BxField('OPPORTUNITY', prefix='FIELDS')
    lead_id = BxField('LEAD_ID', prefix='FIELDS')
    assigned_by = BxField('ASSIGNED_BY_ID', prefix='FIELDS')
    crated_by = BxField('CREATED_BY_ID', prefix='FIELDS')
    modified_by = BxField('MODIFY_BY_ID', prefix='FIELDS')
    created_at = BxDateTime('DATE_CREATE', prefix='FIELDS')
    modified_at = BxDateTime('DATE_MODIFY', prefix='FIELDS')

    _bx_meta = {
        'entity': 'crm.deal'
    }
