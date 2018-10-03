# -*- coding: utf-8 -*-


from bx24_orm.core.bases import BxEntity, BxField


class BaseDeal(BxEntity):
    title = BxField('TITLE', prefix='FIELDS')
    type_id = BxField('TYPE_ID')
    stage = BxField('STAGE_ID')
    opportunity = BxField('OPPORTUNITY')
    lead_id = BxField('LEAD_ID')
    assigned_by = BxField('ASSIGNED_BY_ID')
    crated_by = BxField('CREATED_BY_ID')
    modified_by = BxField('MODIFY_BY_ID')
    created_at = BxField('DATE_CREATE')
    modified_at = BxField('DATE_MODIFY')
    selected_company = BxField('UF_CRM_1499420518')
    companies_with_balance = BxField('UF_CRM_1500376562')
    companies_without_balance = BxField('UF_CRM_1500376578')
    comment = BxField('UF_CRM_582542CDA79E2')

    _bx_meta = {
        'entity': 'crm.deal'
    }
