# -*- coding: utf-8 -*-


from bx24_orm.core.bases import BxEntity
from bx24_orm.core.fields import BxField, BxDateTime, BxBoolean


class BxLead(BxEntity):
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
    opened = BxBoolean('OPENED')
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
    honorific = BxField('HONORIFIC')
    is_return_customer = BxBoolean('IS_RETURN_CUSTOMER')
    has_phone = BxBoolean('HAS_PHONE')
    has_email = BxBoolean('HAS_EMAIL')
    has_imol = BxBoolean('HAS_IMOL')
    status_semantic_id = BxField('STATUS_SEMANTIC_ID')
    utm_source = BxField('UTM_SOURCE')
    utm_medium = BxField('UTM_MEDIUM')
    utm_campaign = BxField('UTM_CAMPAIGN')
    utm_content = BxField('UTM_CONTENT')
    utm_term = BxField('UTM_TERM')
    _bx_meta = {
        'entity': 'crm.lead',
        'default_prefix': 'FIELDS'
    }


class BxDeal(BxEntity):
    title = BxField('TITLE')
    type_id = BxField('TYPE_ID')
    stage = BxField('STAGE_ID')
    probability = BxField('PROBABILITY')
    opportunity = BxField('OPPORTUNITY')
    company_id = BxField('COMPANY_ID')
    contact_id = BxField('CONTACT_ID')
    begin_date = BxDateTime('BEGIN_DATE')
    close_date = BxDateTime('CLOSE_DATE')
    opened = BxBoolean('OPENED')
    closed = BxBoolean('CLOSED')
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
    currency_id = BxField('CURRENCY_ID')
    tax_value = BxField('TAX_VALUE')
    quote_id = BxField('QUOTE_ID')
    location_id = BxField('LOCATION_ID')
    stage_semantic_id = BxField('STAGE_SEMANTIC_ID')
    is_new = BxBoolean('IS_NEW')
    is_recurring = BxBoolean('IS_RECURRING')
    is_return_customer = BxBoolean('IS_RETURN_CUSTOMER')
    is_repeated_approach = BxBoolean('IS_REPEATED_APPROACH')
    source_id = BxField('SOURCE_ID')
    source_description = BxField('SOURCE_DESCRIPTION')
    utm_source = BxField('UTM_SOURCE')
    utm_medium = BxField('UTM_MEDIUM')
    utm_campaign = BxField('UTM_CAMPAIGN')
    utm_content = BxField('UTM_CONTENT')
    utm_term = BxField('UTM_TERM')
    _bx_meta = {
        'entity': 'crm.deal',
        'default_prefix': 'FIELDS'
    }


class BxCompany(BxEntity):
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
    opened = BxBoolean('OPENED')
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
    has_phone = BxBoolean('HAS_PHONE')
    has_email = BxBoolean('HAS_EMAIL')
    has_imol = BxBoolean('HAS_IMOL')
    employees = BxField('EMPLOYEES')
    is_my_company = BxBoolean('IS_MY_COMPANY')
    origin_version = BxField('ORIGIN_VERSION')
    utm_source = BxField('UTM_SOURCE')
    utm_medium = BxField('UTM_MEDIUM')
    utm_campaign = BxField('UTM_CAMPAIGN')
    utm_content = BxField('UTM_CONTENT')
    utm_term = BxField('UTM_TERM')

    _bx_meta = {
        'entity': 'crm.company',
        'default_prefix': 'FIELDS'
    }


class BxContact(BxEntity):
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
    opened = BxBoolean('OPENED')
    comments = BxField('COMMENTS')
    export = BxBoolean('EXPORT')
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
    honorific = BxField('HONORIFIC')
    has_phone = BxBoolean('HAS_PHONE')
    has_email = BxBoolean('HAS_EMAIL')
    has_imol = BxBoolean('HAS_IMOL')
    origin_version = BxField('ORIGIN_VERSION')
    face_id = BxField('FACE_ID')
    utm_source = BxField('UTM_SOURCE')
    utm_medium = BxField('UTM_MEDIUM')
    utm_campaign = BxField('UTM_CAMPAIGN')
    utm_content = BxField('UTM_CONTENT')
    utm_term = BxField('UTM_TERM')

    _bx_meta = {
        'entity': 'crm.contact',
        'default_prefix': 'FIELDS'
    }


class BxActivity(BxEntity):
    owner_id = BxField('OWNER_ID')
    owner_type_id = BxField('OWNER_TYPE_ID')
    type_id = BxField('TYPE_ID')
    provider_id = BxField('PROVIDER_ID')
    provider_type_id = BxField('PROVIDER_TYPE_ID')
    provider_group_id = BxField('PROVIDER_GROUP_ID')
    associated_entity_id = BxField('ASSOCIATED_ENTITY_ID')
    subject = BxField('SUBJECT')
    created = BxDateTime('CREATED')
    last_updated = BxDateTime('LAST_UPDATED')
    start_time = BxDateTime('START_TIME')
    end_time = BxDateTime('END_TIME')
    deadline = BxDateTime('DEADLINE')
    completed = BxBoolean('COMPLETED')
    status = BxField('STATUS')
    responsible_id = BxField('RESPONSIBLE_ID')
    priority = BxField('PRIORITY')
    notify_type = BxField('NOTIFY_TYPE')
    notify_value = BxField('NOTIFY_VALUE')
    description = BxField('DESCRIPTION')
    description_type = BxField('DESCRIPTION_TYPE')
    direction = BxField('DIRECTION')
    location = BxField('LOCATION')
    settings = BxField('SETTINGS')
    originator_id = BxField('ORIGINATOR_ID')
    origin_id = BxField('ORIGIN_ID')
    author_id = BxField('AUTHOR_ID')
    editor_id = BxField('EDITOR_ID')
    provider_params = BxField('PROVIDER_PARAMS')
    provider_data = BxField('PROVIDER_DATA')
    result_mark = BxField('RESULT_MARK')
    result_value = BxField('RESULT_VALUE')
    result_sum = BxField('RESULT_SUM')
    result_currency_id = BxField('RESULT_CURRENCY_ID')
    result_status = BxField('RESULT_STATUS')
    result_stream = BxField('RESULT_STREAM')
    result_source_id = BxField('RESULT_SOURCE_ID')
    autocomplete_rule = BxField('AUTOCOMPLETE_RULE')

    _bx_meta = {
        'entity': 'crm.activity',
        'default_prefix': 'FIELDS'
    }


class BxMeasure(BxEntity):
    code = BxField('CODE')
    measure_title = BxField('MEASURE_TITLE')
    symbol_rus = BxField('SYMBOL_RUS')
    symbol_intl = BxField('SYMBOL_INTL')
    symbol_letter_intl = BxField('SYMBOL_LETTER_INTL')
    is_default = BxBoolean('IS_DEFAULT')

    _bx_meta = {
        'entity': 'crm.measure',
        'default_prefix': 'FIELDS'
    }


class Catalog(BxEntity):
    originator_id = BxField('ORIGINATOR_ID')
    origin_id = BxField('ORIGIN_ID')
    name = BxField('NAME')
    xml_id = BxField('XML_ID')

    _bx_meta = {
        'entity': 'crm.catalog',
        'default_prefix': 'FIELDS'
    }


class BxQuote(BxEntity):
    title = BxField('ENTITY')
    status_id = BxField('STATUS_ID')
    currency_id = BxField('CURRENCY_ID')
    opportunity = BxField('OPPORTUNITY')
    tax_value = BxField('TAX_VALUE')
    company_id = BxField('COMPANY_ID')
    contact_id = BxField('CONTACT_ID')
    mycompany_id = BxField('MYCOMPANY_ID')
    begin_date = BxField('BEGINDATE')
    close_date = BxField('CLOSEDATE')
    assigned_by_id = BxField('ASSIGNED_BY_ID')
    created_by_id = BxField('CREATED_BY_ID')
    modify_by_id = BxField('MODIFY_BY_ID')
    date_create = BxField('DATE_CREATE')
    date_modify = BxField('DATE_MODIFY')
    opened = BxBoolean('OPENED')
    closed = BxBoolean('CLOSED')
    comments = BxField('COMMENTS')
    lead_id = BxField('LEAD_ID')
    deal_id = BxField('DEAL_ID')
    quote_member = BxField('QUOTE_MEMBER')
    content = BxField('CONTENT')
    terms = BxField('TERMS')
    person_type_id = BxField('PERSON_TYPE_ID')
    location_id = BxField('LOCATION_ID')
    client_title = BxField('CLIENT_TITLE')
    client_addr = BxField('CLIENT_ADDR')
    client_contact = BxField('CLIENT_CONTACT')
    client_email = BxField('CLIENT_EMAIL')
    client_phone = BxField('CLIENT_PHONE')
    client_tp_id = BxField('CLIENT_TP_ID')
    client_tpa_id = BxField('CLIENT_TPA_ID')
    utm_source = BxField('UTM_SOURCE')
    utm_medium = BxField('UTM_MEDIUM')
    utm_campaign = BxField('UTM_CAMPAIGN')
    utm_content = BxField('UTM_CONTENT')
    utm_term = BxField('UTM_TERM')

    _bx_meta = {
        'entity': 'crm.quote',
        'default_prefix': 'FIELDS'
    }


class BxDealCategoryStage(BxEntity):
    name = BxField('NAME')
    sort = BxField('SORT')
    status_id = BxField('STATUS_ID')

    _bx_meta = {
        'entity': 'crm.dealcategory.stage',
        'default_prefix': 'FIELDS'
    }


class BxProductSection(BxEntity):
    catalog_id = BxField('CATALOG_ID')
    section_id = BxField('SECTION_ID')
    name = BxField('NAME')
    xml_id = BxField('XML_ID')

    _bx_meta = {
        'entity': 'crm.productsection',
        'default_prefix': 'FIELDS'
    }


class BxAddress(BxEntity):
    type_id = BxField('ENITY_ID')
    entity_type_id = BxField('ENTITY_TYPE_ID')
    entity_id = BxField('ENTITY_ID')
    address_1 = BxField('ADDRESS_1')
    address_2 = BxField('ADDRESS_2')
    city = BxField('CITY')
    postal_code = BxField('POSTAL_CODE')
    region = BxField('REGION')
    province = BxField('PROVINCE')
    country = BxField('COUNTRY')
    country_code = BxField('COUNTRY_CODE')
    anchor_type_id = BxField('ANCHOR_TYPE_ID')
    anchor_id = BxField('ANCHOR_ID')

    _bx_meta = {
        'entity': 'crm.address',
        'default_prefix': 'FIELDS'
    }


class BxRequisite(BxEntity):
    entity_type_id = BxField('ENTITY_TYPE_ID')
    entity_id = BxField('ENTITY_ID')
    preset_id = BxField('PRESET_ID')
    date_create = BxDateTime('DATE_CREATE')
    date_modify = BxDateTime('DATE_MODIFY')
    created_by_id = BxField('CREATED_BY_ID')
    modify_by_id = BxField('MODIFY_BY_ID')
    name = BxField('NAME')
    code = BxField('CODE')
    xml_id = BxField('XML_ID')
    originator_id = BxField('ORIGINATOR_ID')
    active = BxBoolean('ACTIVE')
    sort = BxField('SORT')
    rq_name = BxField('RQ_NAME')
    rq_first_name = BxField('RQ_FIRST_NAME')
    rq_last_name = BxField('RQ_LAST_NAME')
    rq_second_name = BxField('RQ_SECOND_NAME')
    rq_company_name = BxField('RQ_COMPANY_NAME')
    rq_company_full_name = BxField('RQ_COMPANY_FULL_NAME')
    rq_company_reg_date = BxField('RQ_COMPANY_REG_DATE')
    rq_director = BxField('RQ_DIRECTOR')
    rq_accountant = BxField('RQ_ACCOUNTANT')
    rq_ceo_name = BxField('RQ_CEO_NAME')
    rq_ceo_work_pos = BxField('RQ_CEO_WORK_POS')
    rq_contact = BxField('RQ_CONTACT')
    rq_email = BxField('RQ_EMAIL')
    rq_phone = BxField('RQ_PHONE')
    rq_fax = BxField('RQ_FAX')
    rq_ident_doc = BxField('RQ_IDENT_DOC')
    rq_ident_doc_ser = BxField('RQ_IDENT_DOC_SER')
    rq_ident_doc_num = BxField('RQ_IDENT_DOC_NUM')
    rq_ident_doc_pers_num = BxField('RQ_IDENT_DOC_PERS_NUM')
    rq_ident_doc_date = BxField('RQ_IDENT_DOC_DATE')
    rq_ident_doc_issued_by = BxField('RQ_IDENT_DOC_ISSUED_BY')
    rq_ident_doc_dep_code = BxField('RQ_IDENT_DOC_DEP_CODE')
    rq_inn = BxField('RQ_INN')
    rq_kpp = BxField('RQ_KPP')
    rq_usrle = BxField('RQ_USRLE')
    rq_ifsn = BxField('RQ_IFSN')
    rq_ogrn = BxField('RQ_OGRN')
    rq_ogrnip = BxField('RQ_OGRNIP')
    rq_okpo = BxField('RQ_OKPO')
    rq_oktmo = BxField('RQ_OKTMO')
    rq_okved = BxField('RQ_OKVED')
    rq_edrpou = BxField('RQ_EDRPOU')
    rq_drfo = BxField('RQ_DRFO')
    rq_kbe = BxField('RQ_KBE')
    rq_iin = BxField('RQ_IIN')
    rq_bin = BxField('RQ_BIN')
    rq_st_cert_ser = BxField('RQ_ST_CERT_SER')
    rq_st_cert_num = BxField('RQ_ST_CERT_NUM')
    rq_st_cert_date = BxField('RQ_ST_CERT_DATE')
    rq_vat_payer = BxBoolean('RQ_VAT_PAYER')
    rq_vat_id = BxField('RQ_VAT_ID')
    rq_vat_cert_ser = BxField('RQ_VAT_CERT_SER')
    rq_vat_cert_num = BxField('RQ_VAT_CERT_NUM')
    rq_vat_cert_date = BxField('RQ_VAT_CERT_DATE')
    rq_recidence_country = BxField('RQ_RECIDENCE_COUNTRY')
    rq_base_doc = BxField('RQ_BASE_DOC')

    _bx_meta = {
        'entity': 'crm.requisite',
        'default_prefix': 'FIELDS'
    }


class BxRequisiteBankdetail(BxEntity):
    entity_id = BxField('ENTITY_ID')
    country_id = BxField('COUNTRY_ID')
    date_create = BxDateTime('DATE_CREATE')
    date_modify = BxDateTime('DATE_MODIFY')
    name = BxField('NAME')
    code = BxField('CODE')
    xml_id = BxField('XML_ID')
    active = BxBoolean('ACTIVE')
    sort = BxField('SORT')
    rq_bank_name = BxField('RQ_BANK_NAME')
    rq_bank_addr = BxField('RQ_BANK_ADDR')
    rq_bank_route_num = BxField('RQ_BANK_ROUTE_NUM')
    rq_bik = BxField('RQ_BIK')
    rq_mfo = BxField('RQ_MFO')
    rq_acc_name = BxField('RQ_ACC_NAME')
    rq_acc_num = BxField('RQ_ACC_NUM')
    rq_iik = BxField('RQ_IIK')
    rq_acc_currency = BxField('RQ_ACC_CURRENCY')
    rq_cor_acc_num = BxField('RQ_COR_ACC_NUM')
    rq_iban = BxField('RQ_IBAN')
    rq_swift = BxField('RQ_SWIFT')
    rq_bic = BxField('RQ_BIC')
    comments = BxField('COMMENTS')
    originator_id = BxField('ORIGINATOR_ID')

    _bx_meta = {
        'entity': 'crm.requisiste.bankdetail',
        'default_prefix': 'FIELDS'
    }


class BxRequisiteLink(BxEntity):
    entity_type_id = BxField('ENITY_TYPE_ID')
    entity_id = BxField('ENTITY_ID')
    requisite_id = BxField('REQUISITE_ID')
    bank_detail_id = BxField('BANK_DETAIL_ID')
    mc_requisite_id = BxField('MC_REQUISITE_ID')
    mc_bank_detail_id = BxField('MC_BANK_DETAIL_ID')

    _bx_meta = {
        'entity': 'crm.requisite.link',
        'default_prefix': 'FIELDS'
    }


class BxRequisitePreset(BxEntity):
    entity_type_id = BxField('ENTITY_TYPE_ID')
    country_id = BxField('COUNTRY_ID')
    name = BxField('NAME')
    date_create = BxDateTime('DATE_CREATE')
    date_modify = BxDateTime('DATE_MODIFY')
    created_by_id = BxField('CREATED_BY_ID')
    modify_by_id = BxField('MODIFY_BY_ID')
    active = BxBoolean('ACTIVE')
    sort = BxField('SORT')
    xml_id = BxField('XML_ID')

    _bx_meta = {
        'entity': 'crm.requisite.preset',
        'default_prefix': 'FIELDS'
    }


class BxInvoiceStatus(BxEntity):
    entity_id = BxField('ENTITY_ID')
    status_id = BxField('STATUS_ID')
    name = BxField('NAME')
    name_init = BxField('NAME_INIT')
    sort = BxField('SORT')
    system = BxBoolean('SYSTEM')

    _bx_meta = {
        'entity': 'crm.invoice.status',
        'default_prefix': 'FIELDS'
    }


class BxDealCategory(BxEntity):
    created_date = BxDateTime('CREATED_DATE')
    name = BxDateTime('NAME')
    is_locked = BxBoolean('IS_LOCKED')
    sort = BxField('SORT')

    _bx_meta = {
        'entity': 'crm.dealcategory'
    }


class BxInvoice(BxEntity):
    account_number = BxField('ACCOUNT_NUMBER')
    comments = BxField('COMMENTS')
    currency = BxField('CURRENCY')
    date_bill = BxDateTime('DATE_BILL')
    date_insert = BxDateTime('DATE_INSERT')
    date_marked = BxDateTime('DATE_MARKED')
    date_pay_before = BxDateTime('DATE_PAY_BEFORE')
    date_payed = BxDateTime('DATE_PAYED')
    date_status = BxDateTime('DATE_STATUS')
    date_update = BxDateTime('DATE_UPDATE')
    created_by = BxField('CREATED_BY')
    emp_payed_id = BxField('EMP_PAYED_ID')
    emp_status_id = BxField('EMP_STATUS_ID')
    lid = BxField('LID')
    xml_id = BxField('XML_ID')
    order_topic = BxField('ORDER_TOPIC')
    pay_system_id = BxField('PAY_SYSTEM_ID')
    pay_voucher_date = BxDateTime('PAY_VOUCHER_DATE')
    pay_voucher_num = BxField('PAY_VOUCHER_NUM')
    payed = BxBoolean('PAYED')
    person_type_id = BxField('PERSON_TYPE_ID')
    price = BxField('PRICE')
    reason_marked = BxField('REASON_MARKED')
    responsible_email = BxField('RESPONSIBLE_EMAIL')
    responsible_id = BxField('RESPONSIBLE_ID')
    responsible_last_name = BxField('RESPONSIBLE_LAST_NAME')
    responsible_login = BxField('RESPONSIBLE_LOGIN')
    responsible_name = BxField('RESPONSIBLE_NAME')
    responsible_personal_photo = BxField('RESPONSIBLE_PERSONAL_PHOTO')
    responsible_second_name = BxField('RESPONSIBLE_SECOND_NAME')
    responsible_work_position = BxField('RESPONSIBLE_WORK_POSITION')
    status_id = BxField('STATUS_ID')
    tax_value = BxField('TAX_VALUE')
    company_id = BxField('UF_COMPANY_ID')
    contact_id = BxField('UF_CONTACT_ID')
    mycompany_id = BxField('UF_MYCOMPANY_ID')
    deal_id = BxField('UF_DEAL_ID')
    quote_id = BxField('UF_QUOTE_ID')
    user_description = BxField('USER_DESCRIPTION')
    invoice_properties = BxField('INVOICE_PROPERTIES')
    product_rows = BxField('PRODUCT_ROWS')

    _bx_meta = {
        'entity': 'crm.invoice',
        'default_prefix': 'FIELDS'
    }


class BxPaySystem(BxEntity):
    name = BxField('NAME')
    active = BxBoolean('ACTIVE')
    sort = BxField('SORT')
    description = BxField('DESCRIPTION')
    person_type_id = BxField('PERSON_TYPE_ID')
    action_file = BxField('ACTION_FILE')
    handler = BxField('HANDLER')
    handler_code = BxField('HANDLER_CODE')
    handler_name = BxField('HANDLER_NAME')

    _bx_meta = {
        'entity': 'crm.paysystem',
        'default_prefix': 'FIELDS'
    }


class BxPersonType(BxEntity):
    name = BxField('NAME')

    _bx_meta = {
        'entity': 'crm.persontype',
        'default_prefix': 'FIELDS'
    }


class BxProduct(BxEntity):
    name = BxField('NAME')
    active = BxBoolean('ACTIVE')
    preview_picture = BxField('PREVIEW_PICTURE')
    detail_picture = BxField('DETAIL_PICTURE')
    sort = BxField('SORT')
    xml_id = BxField('XML_ID')
    catalog_id = BxField('CATALOG_ID')
    section_id = BxField('SECTION_ID')
    description = BxField('DESCRIPTION')
    description_type = BxField('DESCRIPTION_TYPE')
    price = BxField('PRICE')
    currency_id = BxField('CURRENCY_ID')
    vat_id = BxField('VAT_ID')
    vat_included = BxField('VAT_INCLUDED')
    measure = BxField('MEASURE')

    _bx_meta = {
        'entity': 'crm.product',
        'default_prefix': 'FIELDS'
    }


class BxProductProperty(BxEntity):
    iblock_id = BxField('IBLOCK_ID')
    name = BxField('NAME')
    active = BxBoolean('ACTIVE')
    sort = BxField('SORT')
    default_value = BxField('DEFAULT_VALUE')
    property_type = BxField('PROPERTY_TYPE')
    row_count = BxField('ROW_COUNT')
    col_count = BxField('COL_COUNT')
    multiple = BxBoolean('MULTIPLE')
    xml_id = BxField('XML_ID')
    file_type = BxField('FILE_TYPE')
    link_iblock_id = BxField('LINK_IBLOCK_ID')
    is_required = BxBoolean('IS_REQUIRED')
    user_type = BxField('USER_TYPE')
    user_type_settings = BxField('USER_TYPE_SETTINGS')
    values = BxField('VALUES')

    _bx_meta = {
        'entity': 'crm.product.property',
        'default_prefix': 'FIELDS'
    }


class BxProductPropertyTypes(BxEntity):
    property_type = BxField('PROPERTY_TYPE')
    user_type = BxField('USER_TYPE')
    description = BxField('DESCRIPTION')

    _bx_meta = {
        'entity': 'crm.product.property.types'
    }
