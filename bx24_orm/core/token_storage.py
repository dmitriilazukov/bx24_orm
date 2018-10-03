# -*- coding: utf-8 -*-

import requests
import shelve


class DefaultTokenStorage(object):
    def __init__(self, bx_settings):
        self.bx_settings = bx_settings

    def save_token(self, domain, token, refresh_token):
        storage = shelve.open(self.bx_settings.TOKEN_STORAGE_FILENAME)
        storage[domain] = {'token': token, 'refresh_token': refresh_token}
        storage.close()

    def get_token(self, domain):
        # type: (str) -> str
        storage = shelve.open(self.bx_settings.TOKEN_STORAGE_FILENAME)
        result = storage[domain]['token']
        storage.close()
        return result

    def refresh_token(self, domain):
        # type: (str) -> str
        url = 'https://{}.bitrix24.ru/oauth/token/'.format(domain)
        storage = shelve.open(self.bx_settings.TOKEN_STORAGE_FILENAME)
        domain_options = self.bx_settings.BX24_DOMAIN_SETTINGS[domain]
        params = {
            'client_id': domain_options['client_id'],
            'client_secret': domain_options['client_secret'],
            'grant_type': 'refresh_token',
            'refresh_token': storage[domain]['refresh_token']
        }
        response = requests.get(url, params)
        result = response.json()
        token, refresh_token = result['access_token'], result['refresh_token']
        self.save_token(domain, token, refresh_token)
        return token
