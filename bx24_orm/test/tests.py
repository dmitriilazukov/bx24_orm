# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase
from datetime import datetime

from bx24_orm.core.bx_interface import BxQuery, BxBatch, BxBatchCommand, BxQueryBuilder
from bx24_orm.core.bases import BxEntity
from bx24_orm.core.fields import BxField, BxDateTime
from bx24_orm.core import settings, token_storage
from bx24_orm.core.exceptions.code_exceptions import (TokenNotFoundException, InvalidQueryException,
                                                      InvalidTokenException)
from bx24_orm.enitiy.crm import BxDeal, BxLead, BxCompany

GLOBAL_TEST_LEAD = settings.TEST_LEAD
GLOBAL_TEST_DEAL = settings.TEST_DEAL
GLOBAL_TEST_COMPANY = settings.TEST_COMPANY
GLOBAL_TEST_INVOICE = settings.TEST_INVOICE


class BxQueryBuilderTest(TestCase):
    def setUp(self):
        self.TEST_IDS = [1, 2]
        self.TEST_NAME = 'TE'
        self.TEST_NUM = 35

    def testQuery(self):
        builder = BxQueryBuilder()
        expected_dict = {
            'FILTER[ID][0]': self.TEST_IDS[0],
            'FILTER[ID][1]': self.TEST_IDS[1],
            'FILTER[%TITLE]': self.TEST_NAME,
            'FILTER[>=ID]': self.TEST_NUM,
            'FILTER[<=ID]': self.TEST_NUM,
            'FILTER[>ID]': self.TEST_NUM,
            'FILTER[<ID]': self.TEST_NUM,
            'FILTER[SOME_FIELD]': self.TEST_NUM,
            'SELECT[0]': 'ID',
            'SELECT[1]': 'TITLE',
            'ORDER[ID]': 'DESC',
            'ORDER[TITLE]': 'ASC'
        }
        builder = builder.filter(id__in=self.TEST_IDS)
        builder = builder.filter(title__contains=self.TEST_NAME)
        builder = builder.filter(id__gte=self.TEST_NUM)
        builder = builder.filter(id__lte=self.TEST_NUM, id__lt=self.TEST_NUM, id__gt=self.TEST_NUM)
        builder = builder.filter(some_field=self.TEST_NUM)
        builder = builder.select('id', 'title')
        builder = builder.order('-id').order('title')
        self.assertEqual(expected_dict, builder.build())

    def testErrors(self):
        builder = BxQueryBuilder()
        self.assertRaises(ValueError, builder.filter, **{'gte': 'qwe'})
        self.assertRaises(ValueError, builder.filter, **{'id__invalid_option': 'qwe'})
        self.assertRaises(ValueError, builder.filter, **{'id__value__gte': 'qwe'})
        self.assertRaises(ValueError, builder.filter, **{'id__in': '1,2,3,4'})


class BxBatchTest(TestCase):
    def setUp(self):
        self.token = token_storage.get_token(settings.default_domain)
        self.domain = settings.default_domain
        self.TEST_LEAD = GLOBAL_TEST_LEAD
        self.TEST_DEAL = GLOBAL_TEST_DEAL
        self.TEST_COMPANY = GLOBAL_TEST_COMPANY
        self.test_queries = [('crm.lead.get', {'ID': self.TEST_LEAD}, 'raw_lead'),
                             ('crm.deal.get', {'ID': self.TEST_DEAL}, 'raw_deal'),
                             ('crm.company.get', {'ID': self.TEST_COMPANY}, 'raw_company')]

    def testConstructorFromBxBatchCommand(self):
        batches = []
        expected_batches = {}
        for q, p, n in self.test_queries:
            expected_batches.update({
                'cmd[{}]'.format(n): '{}?ID={}'.format(q, p['ID'])
            })
            batches.append(BxBatchCommand(q, p, n))
        batch = BxBatch(batches, self.token, self.domain)
        created_commands = batch.commands
        for e in expected_batches:
            self.assertEqual(created_commands[e], expected_batches[e])

    def testConstructorFromBxQueryCommand(self):
        queries = []
        expected_queries = {}
        for q, p, n in self.test_queries:
            expected_queries.update({
                'cmd[{}]'.format(n): '{}?ID={}'.format(q, p['ID'])
            })
            queries.append(BxQuery(q, p, cmd_name=n, domain=self.domain))
        batch = BxBatch(queries, self.token, self.domain)
        created_commands = batch.commands
        for e in expected_queries:
            self.assertEqual(created_commands[e], expected_queries[e])

    def testNotAsciiParameters(self):
        defaut_domain = settings.default_domain
        token = token_storage.get_token(defaut_domain)
        command = BxQuery('crm.lead.list', {'FILTER[%NAME]': 'неаскистрока', 'auth': token}, defaut_domain)
        result = command.call()
        self.assertEqual(result.total, 0)

    def testConstructorFail(self):
        expected_queries = {}
        queries = []
        for q, p, n in self.test_queries:
            expected_queries.update({
                'cmd[{}]'.format(n): '{}?ID={}'.format(q, p['ID'])
            })
            queries.append(BxQuery(q, p, cmd_name=n, domain=self.domain))
        invalid_query = {'crm.lead.get': {'ID': 1234}}
        queries.append(invalid_query)
        self.assertRaises(ValueError, BxBatch, queries, self.token, self.domain)

    def testSuccessfulQuery(self):
        batches = []
        for q, p, n in self.test_queries:
            batches.append(BxBatchCommand(q, p, n))
        batch = BxBatch(batches, self.token, self.domain)
        result = batch.call()
        for q, p, n in self.test_queries:
            self.assertEqual(result.result[n]['ID'], str(p['ID']))
            self.assertEqual(result[n].result['ID'], str(p['ID']))
            self.assertFalse(result[n].error)
            self.assertEqual(result[n].total, 1)
            self.assertEqual(result[n].result_next, 0)

    def testFailedQuery(self):
        batches = []
        for q, p, n in self.test_queries:
            batches.append(BxBatchCommand(q, p, n))
        batch = BxBatch(batches, self.token + 'INVALID_TOKEN', self.domain)
        result = batch.safe_call()
        self.assertTrue(result.error)
        self.assertFalse(result.result)
        self.assertFalse(result.result_next)
        self.assertFalse(result.result_total)


class BxQueryTest(TestCase):
    def setUp(self):
        self.TEST_LEAD_ID = GLOBAL_TEST_LEAD
        self.TEST_LEAD_QUERY = 'crm.lead.get'
        self.domain = settings.default_domain
        self.token = token_storage.get_token(settings.default_domain)

    def testTokenNotProvided(self):
        params = {'ID': self.TEST_LEAD_ID}
        query = BxQuery(self.TEST_LEAD_QUERY, params, self.domain)
        self.assertRaises(TokenNotFoundException, query.call)

    def testSuccessfulQuery(self):
        params = {'ID': self.TEST_LEAD_ID, 'auth': self.token}
        query = BxQuery(self.TEST_LEAD_QUERY, params, self.domain)
        self.assertEqual(query.call().result['ID'], self.TEST_LEAD_ID)

    def testInvalidQuery(self):
        params = {'ID': self.TEST_LEAD_ID, 'auth': self.token}
        query = BxQuery(self.TEST_LEAD_QUERY + 'MESSED_UP_QUERY', params, self.domain)
        self.assertRaises(InvalidQueryException, query.call)

    def testInvalidToken(self):
        params = {'ID': self.TEST_LEAD_ID, 'auth': self.token + 'INVALID_TOKEN'}
        query = BxQuery(self.TEST_LEAD_QUERY, params, self.domain)
        self.assertRaises(InvalidTokenException, query.call)

    def testSafeCall(self):
        params = {'ID': self.TEST_LEAD_ID, 'auth': self.token + 'INVALID_TOKEN'}
        query = BxQuery(self.TEST_LEAD_QUERY, params, self.domain)
        result = query.safe_call()
        self.assertEqual(result.result, {})
        self.assertEqual(result.result_next, 0)
        self.assertEqual(result.total, 0)
        self.assertTrue(result.error['error'])
        params = {'ID': self.TEST_LEAD_ID, 'auth': self.token}
        query = BxQuery(self.TEST_LEAD_QUERY, params, self.domain)
        result = query.safe_call()
        self.assertEqual(result.result['ID'], self.TEST_LEAD_ID)
        self.assertEqual(result.result_next, 0)
        self.assertEqual(result.total, 1)

    def testAsBatch(self):
        params = {'ID': self.TEST_LEAD_ID, 'auth': self.token}
        cmd_name = 'LEAD_GET_COMMAND'
        expected = {
            'cmd[{}]'.format(cmd_name): '{query}?ID={ID}&auth={auth}'.format(query=self.TEST_LEAD_QUERY, **params)}
        query = BxQuery(self.TEST_LEAD_QUERY, params, self.domain, cmd_name=cmd_name)
        self.assertEqual(expected, query.as_batch())


class BasesAndMixinsTest(TestCase):
    def setUp(self):
        self.TEST_ID = 1
        self.SECOND_TEST_ID = 2
        self.PHONE = [{'TYPE': 'WORK', 'VALUE': ['1234', '456']}, {'TYPE': 'HOME', 'VALUE': '4567'}]
        self.CONVERTED_COMMAND = {
            'FIELDS[PHONE][0][TYPE]': 'WORK',
            'FIELDS[PHONE][0][VALUE][0]': '1234',
            'FIELDS[PHONE][0][VALUE][1]': '456',
            'FIELDS[PHONE][1][TYPE]': 'HOME',
            'FIELDS[PHONE][1][VALUE]': '4567'
        }

    def testBxFields(self):
        now = datetime.now()
        dtime_format = '%Y-%m-%dT%H:%M:%S.%f'

        class WithBxFields(BxEntity):
            _bx_meta = {
                'default_prefix': 'FIELDS'
            }
            id = BxField('ID', prefix='FIELDS')
            phone = BxField('PHONE', prefix='FIELDS')
            dtime = BxDateTime('DATETIME')

        dealInstance = BxDeal()
        wbf = WithBxFields(ID=self.TEST_ID, PHONE=self.PHONE, DATETIME=now.strftime(dtime_format), prefix='FIELDS')
        self.assertNotEqual(dealInstance._bx_meta, wbf._bx_meta)
        self.assertFalse(wbf.changed_fields)
        self.assertEqual(wbf.id.value, self.TEST_ID)
        wbf.id = self.SECOND_TEST_ID
        self.assertEqual(wbf.id.value, self.SECOND_TEST_ID)
        self.assertEqual(wbf.changed_fields[0], 'id')
        self.assertEqual(wbf.phone.to_bitrix, self.CONVERTED_COMMAND)
        wbf.phone.value[0] = 'CHANGED'
        self.assertNotEqual(wbf.phone.value[0], 'CHANGED')
        to_change = wbf.phone.value
        to_change[0] = 'CHANGED'
        wbf.phone = to_change
        self.assertEqual(wbf.phone.value[0], 'CHANGED')
        self.assertEqual(wbf.changed_fields[1], 'phone')
        self.assertEqual(wbf.dtime.to_bitrix, {'FIELDS[DATETIME]': now.strftime(dtime_format)})
        self.assertNotEqual(wbf.phone.value, wbf.id.value)
        self.assertRaises(ValueError, wbf.__setattr__, 'dtime', 'random value')
        self.assertEqual(len(wbf.changed_fields), 2)
        wbf.dtime = now.strftime('%Y-%m-%dT%H:%M:%S.%f')
        self.assertEqual(wbf.changed_fields[2], 'dtime')
        self.assertEqual(wbf.dtime.value, now)
        self.assertEqual(len(wbf.changed_fields), 3)
        wbf.dtime = now
        self.assertEqual(len(wbf.changed_fields), 3)
        self.assertEqual(wbf.dtime.value, now)
        self.assertEqual(wbf.dtime.to_bitrix, {'FIELDS[DATETIME]': now.strftime('%Y-%m-%dT%H:%M:%S.%f')})


class BaseEntityCRUDTestMixin(object):

    def testCreateAndUpdate(self):
        import random
        import string
        before_create = len(self.entity_cls.objects.all())
        initial_entity = self.entity_cls.get(self.entity_id)
        entity = self.entity_cls(**self.entity_kwargs)
        entity.save()
        initial_entity = self.entity_cls.get(self.entity_id)
        self.assertNotEqual(entity.title(), initial_entity.title())
        created_entity = self.entity_cls.get(entity.id())
        BaseEntityCRUDTestMixin.created_entity_id = entity.id()
        self.assertNotEqual(created_entity.id(), initial_entity.id())
        for k in self.entity_kwargs:
            v = self.entity_kwargs[k]
            self.assertEqual(v, getattr(created_entity, k)())
        after_create = len(self.entity_cls.objects.all())
        self.assertNotEqual(before_create, after_create)
        self.assertEqual(after_create, before_create + 1)
        created_entity = self.entity_cls.get(BaseEntityCRUDTestMixin.created_entity_id)
        first_kwarg = next(iter(self.entity_kwargs))
        random_line = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        setattr(created_entity, first_kwarg, random_line)
        created_entity.save()
        test_created_entity = self.entity_cls.get(BaseEntityCRUDTestMixin.created_entity_id)
        self.assertEqual(test_created_entity.id(), created_entity.id())
        self.assertEqual(getattr(test_created_entity, first_kwarg)(), random_line)

    def testDelete(self):
        before_delete = len(self.entity_cls.objects.all())
        created_entity = self.entity_cls.get(BaseEntityCRUDTestMixin.created_entity_id)
        created_entity.delete()
        after_delete = len(self.entity_cls.objects.all())
        self.assertNotEqual(before_delete, after_delete)
        self.assertEqual(before_delete, after_delete + 1)


class BxLeadTests(TestCase, BaseEntityCRUDTestMixin):
    def setUp(self):
        self.entity_id = GLOBAL_TEST_LEAD
        self.entity_cls = BxLead
        self.entity_kwargs = {'title': 'NEW_TEST_LEAD', 'utm_term': 'NEW_UTM_TERM'}

    def testCreateAndUpdate(self):
        super(BxLeadTests, self).testCreateAndUpdate()

    def testDelete(self):
        super(BxLeadTests, self).testDelete()


class BxDealTests(TestCase, BaseEntityCRUDTestMixin):
    def setUp(self):
        self.entity_id = GLOBAL_TEST_DEAL
        self.entity_cls = BxDeal
        self.entity_kwargs = {'title': 'NEW_TEST_DEAL', 'utm_term': 'NEW_UTM_TERM'}

    def testCreateAndUpdate(self):
        super(BxDealTests, self).testCreateAndUpdate()

    def testDelete(self):
        super(BxDealTests, self).testDelete()


class BxCompanyTests(TestCase, BaseEntityCRUDTestMixin):
    def setUp(self):
        self.entity_id = GLOBAL_TEST_COMPANY
        self.entity_cls = BxCompany
        self.entity_kwargs = {'title': 'NEW_TEST_COMPANY', 'utm_term': 'NEW_UTM_TERM'}

    def testCreateAndUpdate(self):
        super(BxCompanyTests, self).testCreateAndUpdate()

    def testDelete(self):
        super(BxCompanyTests, self).testDelete()


# class BxInvoiceTests(TestCase, BaseEntityCRUDTestMixin):
#     def setUp(self):
#         self.entity_id = GLOBAL_TEST_INVOICE
#         self.entity_cls = BxInvoice
#         self.entity_kwargs = {'order_topic': 'NEW_TEST_INVOICE'}
#
#     def testCreateAndUpdate(self):
#         super(BxInvoiceTests, self).testCreateAndUpdate()
#
#     def testDelete(self):
#         super(BxInvoiceTests, self).testDelete()


class DealCompanyLeadCombinationTest(TestCase):
    def setUp(self):
        self.lead_id = GLOBAL_TEST_LEAD
        self.deal_id = GLOBAL_TEST_DEAL
        self.company_id = GLOBAL_TEST_COMPANY

    def testIntegration(self):
        lead = BxLead.get(self.lead_id)
        deal = BxDeal.get(self.deal_id)
        company = BxCompany.get(self.company_id)
        self.assertEqual(company.lead_id(), lead.id())
        self.assertEqual(deal.lead_id(), lead.id())
        self.assertEqual(deal.company_id(), company.id())
        self.assertEqual(lead.company_id(), company.id())


class Deal(BxDeal):
    custom_field = BxField('UF_CRM_1539088441')


class Lead(BxLead):
    custom_field = BxField('UF_CRM_1539088367')


class Company(BxCompany):
    custom_field = BxField('UF_CRM_1539088478')


class TestLead(TestCase, BaseEntityCRUDTestMixin):
    def setUp(self):
        self.entity_id = GLOBAL_TEST_LEAD
        self.entity_cls = Lead
        self.entity_kwargs = {'title': 'NEW_TEST_LEAD', 'utm_term': 'UTM_TERM'}

    def testCreateAndUpdate(self):
        super(TestLead, self).testCreateAndUpdate()

    def testDelete(self):
        super(TestLead, self).testDelete()
