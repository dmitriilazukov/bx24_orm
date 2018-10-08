# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase
from datetime import datetime

from bx24_orm.core.bx_interface import BxQuery, BxBatch, BxBatchCommand, BxQueryBuilder
from bx24_orm.core.bases import BxEntity
from bx24_orm.core.fields import BxField, BxDateTime
from bx24_orm.core import settings, token_storage
from bx24_orm.core.exceptions.code_exceptions import *
from bx24_orm.core.exceptions.bx_exceptions import *
from bx24_orm.enitiy.crm import BxDeal, BxLead


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
        self.TEST_LEAD = 1
        self.TEST_DEAL = 1
        self.TEST_COMPANY = 1
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
        self.TEST_LEAD_ID = '1'
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
        self.assertEqual(result.result, None)
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


class BxEntityTest(TestCase):
    def setUp(self):
        self.TEST_DEAL = 1

    def testDealFetch(self):
        deal = BxDeal.get(self.TEST_DEAL)
        self.assertEqual(deal.id.value, self.TEST_DEAL.__str__())
        self.assertEqual(deal.title.value, 'TEST_DEAL')
        deal.utm_content = 'TEST_UTM_CONTENT'
        self.assertEqual(len(deal.changed_fields), 1)
        deal.save()

    def testDealCreate(self):
        new_title = 'NEW_TEST_DEAL'
        utm_content = 'TEST_UTM_CONTENT'
        current_deals = BxDeal.objects.all()
        current_length = len(current_deals)
        deal = BxDeal(title=new_title, utm_content=utm_content)
        deal.save()
        self.assertNotEqual(deal.id(), None)
        self.assertEqual(deal.utm_content(), utm_content)
        new_deal = BxDeal.get(deal.id)
        self.assertEqual(deal.title(), new_deal.title())
        self.assertNotEqual(deal.date_create(), new_deal.date_create())
        self.assertEqual(deal.id().__str__(), new_deal.id())
        deal.delete()
        current_deals = BxDeal.objects.all()
        self.assertEqual(current_length, len(current_deals))

    def testCreateLeadAndDealMixed(self):
        new_title = 'NEW_TEST_LEAD'
        current_leads = BxLead.objects.all()
        current_len = len(current_leads)
        lead = BxLead(title=new_title)
        lead.save()
        first_id = lead.id()
        test_address = 'TEST_ADDRESS'
        lead.address = test_address
        self.assertEqual(len(lead.changed_fields), 1)
        self.assertEqual(lead.changed_fields[0], 'address')
        lead.save()
        self.assertEqual(first_id, lead.id())
        created = BxLead.get(lead.id())
        self.assertEqual(lead.title(), created.title())
        deal = BxDeal(title=new_title)
        deal.save()
        created_deal = BxDeal.get(deal.id())
        self.assertEqual(deal.title(), created_deal.title())
        created.delete()
        created_deal.delete()
        current_leads = BxLead.objects.all()
        self.assertEqual(current_len, len(current_leads))
