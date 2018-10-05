# -*- coding: utf-8 -*-


from bx24_orm.core.bases import BxEntity
from bx24_orm.core.fields import BxField, BxDateTime


class BaseLead(BxEntity):
    title = BxField('TITLE')
    name = BxField('NAME')
    second_name = BxField('SECOND_NAME')
    last_name = BxField('LAST_NAME')
    company_title = BxField('COMPANY_TITLE')
    source_id = BxField('SOURCE_ID')
    source_description = BxField('SOURCE_DESCRIPTION')
    status_id = BxField('STATUS_ID')
    status_description = BxField('STATUS_DESCRIPTION')
    post = BxField('POST')
    address = BxField('ADDRESS')
    address_2 = BxField('ADDRESS_2')
    address_city = BxField('ADDRESS_CITY')
    address_postal_code = BxField('ADDRESS_POSTAL_CODE')
    address_region = BxField('ADDRESS_REGION')
    address_province = BxField('ADDRESS_PROVINCE')
    address_country = BxField('ADDRESS_COUNTRY')
    address_country_code = BxField('ADDRESS_COUNTRY_CODE')
    currency_id = BxField('CURRENCY_ID')
    opportunity = BxField('OPPORTUNITY')
    opened = BxField('OPENED')
    comments = BxField('COMMENTS')
    assigned_by_id = BxField('ASSIGNED_BY_ID')
    created_by_id = BxField('CREATED_BY_ID')
    modify_by_id = BxField('MODIFY_BY_ID')
    date_create = BxDateTime('DATE_CREATE')
    date_modify = BxDateTime('DATE_MODIFY')
    company_id = BxField('COMPANY_ID')
    contact_id = BxField('CONTACT_ID')
    date_closed = BxDateTime('DATE_CLOSED')
    phone = BxField('PHONE')
    email = BxField('EMAIL')
    web = BxField('WEB')
    im = BxField('IM')
    originator_id = BxField('ORIGINATOR_ID')
    origin_id = BxField('ORIGIN_ID')

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
    company_id = BxField('COMPANY_ID')
    contact_id = BxField('CONTACT_ID')
    begin_date = BxDateTime('BEGIN_DATE')
    close_date = BxDateTime('CLOSE_DATE')
    opened = BxField('OPENED')
    closed = BxField('CLOSED')
    comments = BxField('COMMENTS')
    assigned_by_id = BxField('ASSIGNED_BY_ID')
    crated_by_id = BxField('CREATED_BY_ID')
    modify_by_id = BxField('MODIFY_BY_ID')
    date_create = BxDateTime('DATE_CREATE')
    date_modify = BxDateTime('DATE_MODIFY')
    lead_id = BxField('LEAD_ID')
    additional_info = BxField('ADDITIONAL_INFO')
    originator_id = BxField('ORIGINATOR_ID')
    origin_id = BxField('ORIGIN_ID')
    category_id = BxField('CATEGORY_ID')

    _bx_meta = {
        'entity': 'crm.deal',
        'default_prefix': 'FIELDS'
    }


class BaseCompany(BxEntity):
    title = BxField('TITLE')
    company_type = BxField('COMPANY_TYPE')
    logo = BxField('LOGO')
    address = BxField('ADDRESS')
    address_2 = BxField('ADDRESS_2')
    address_city = BxField('ADDRESS_CITY')
    address_postal_code = BxField('ADDRESS_POSTAL_CODE')
    address_region = BxField('ADDRESS_REGION')
    address_province = BxField('ADDRESS_PROVINCE')
    address_country = BxField('ADDRESS_COUNTRY')
    address_country_code = BxField('ADDRESS_COUNTRY_CODE')
    reg_address = BxField('REG_ADDRESS')
    reg_address_2 = BxField('REG_ADDRESS_2')
    reg_address_city = BxField('REG_ADDRESS_CITY')
    reg_address_postal_code = BxField('REG_ADDRESS_POSTAL_CODE')
    reg_address_region = BxField('REG_ADDRESS_REGION')
    reg_address_province = BxField('REG_ADDRESS_PROVINCE')
    reg_address_country = BxField('REG_ADDRESS_COUNTRY')
    reg_address_country_code = BxField('REG_ADDRESS_COUNTRY_CODE')
    address_legal = BxField('ADDRESS_LEGAL')
    banking_details = BxField('BANKING_DETAILS')
    industry = BxField('INDUSTRY')
    currency_id = BxField('CURRENCY_ID')
    revenue = BxField('REVENUE')
    opened = BxField('OPENED')
    comments = BxField('COMMENTS')
    assigned_by_id = BxField('ASSIGNED_BY_ID')
    created_by_id = BxField('CREATED_BY_ID')
    modify_by_id = BxField('MODIFY_BY_ID')
    date_create = BxDateTime('DATE_CREATE')
    date_modify = BxDateTime('DATE_MODIFY')
    lead_id = BxField('LEAD_ID')
    originator_id = BxField('ORIGINATOR_ID')
    origin_id = BxField('ORIGIN_ID')
    phone = BxField('PHONE')
    email = BxField('EMAIL')
    web = BxField('WEB')
    im = BxField('IM')

    _bx_meta = {
        'entity': 'crm.company',
        'default_prefix': 'FIELDS'
    }


class BaseContact(BxEntity):
    name = BxField('NAME')
    second_name = BxField('SECOND_NAME')
    last_name = BxField('LAST_NAME')
    photo = BxField('PHOTO')
    birthdate = BxField('BIRTHDATE')
    type_id = BxField('TYPE_ID')
    source_id = BxField('SOURCE_ID')
    source_description = BxField('SOURCE_DESCRIPTION')
    post = BxField('POST')
    address = BxField('ADDRESS')
    address_2 = BxField('ADDRESS_2')
    address_city = BxField('ADDRESS_CITY')
    address_postal_code = BxField('ADDRESS_POSTAL_CODE')
    address_region = BxField('ADDRESS_REGION')
    address_province = BxField('ADDRESS_PROVINCE')
    address_country = BxField('ADDRESS_COUNTRY')
    address_country_code = BxField('ADDRESS_COUNTRY_CODE')
    opened = BxField('OPENED')
    comments = BxField('COMMENTS')
    export = BxField('EXPORT')
    assigned_by_id = BxField('ASSIGNED_BY_ID')
    created_by_id = BxField('CREATED_BY_ID')
    modify_by_id = BxField('MODIFY_BY_ID')
    date_create = BxDateTime('DATE_CREATE')
    date_modify = BxDateTime('DATE_MODIFY')
    company_id = BxField('COMPANY_ID')
    lead_id = BxField('LEAD_ID')
    phone = BxField('PHONE')
    email = BxField('EMAIL')
    web = BxField('WEB')
    im = BxField('IM')
    originator_id = BxField('ORIGINATOR_ID')
    origin_id = BxField('ORIGIN_ID')

    _bx_meta = {
        'entity': 'crm.contact',
        'default_prefix': 'FIELDS'
    }
