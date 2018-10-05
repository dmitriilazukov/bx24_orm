# -*- coding: utf-8 -*-


from bx24_orm.core.bases import BxEntity
from bx24_orm.core.fields import BxField, BxDateTime


class BaseLead(BxEntity):
    title = BxField('TITLE')
    _bx_meta = {
        'entity': 'crm.lead',
        'default_prefix': 'FIELDS'
    }


class BaseDeal(BxEntity):
    title = BxField('TITLE')
    type_id = BxField('TYPE_ID')
    stage = BxField('STAGE_ID')
    probability = BxField('PROBABILITY')
    opportunity = BxField('OPPORTUNITY')
    lead_id = BxField('LEAD_ID')
    assigned_by = BxField('ASSIGNED_BY_ID')
    crated_by = BxField('CREATED_BY_ID')
    modified_by = BxField('MODIFY_BY_ID')
    created_at = BxDateTime('DATE_CREATE')
    modified_at = BxDateTime('DATE_MODIFY')

    _bx_meta = {
        'entity': 'crm.deal',
        'default_prefix': 'FIELDS'
    }
