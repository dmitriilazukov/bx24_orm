# -*- coding: utf-8 -*-

import requests
import shelve

from os import path


class BaseTokenStorage(object):
    def __init__(self, *args, **kwargs):
        super(BaseTokenStorage, self).__init__(*args, **kwargs)

    def save_token(self, domain, token, refresh_token):
        """
        Save token and refresh token
        :param domain: your bitrix 3-d level domain
        :param token: access_token
        :param refresh_token: refresh_token
        """
        raise NotImplementedError()

    def get_token(self, domain):
        """
        Gets access token
        :rtype: str
        :param domain: your bitrix 3-d level domain
        """
        raise NotImplementedError()

    def get_refresh_token(self, domain):
        """
        Gets refresh token
        :rtype: str
        :param domain: your bitrix 3-d level domain
        """
        raise NotImplementedError()

    def refresh_token(self, domain):
        """
        Gets access token
        :rtype: str
        :param domain: your bitrix 3-d level domain
        """
        raise NotImplementedError()

    def get_client_credentials(self, domain):
        """
        Gets dict of client_id and client_secret credentials
        :rtype: dict
        :param domain: your bitrix 3-d level domain
        """
        raise NotImplementedError()


class DefaultTokenStorage(BaseTokenStorage):
    def __init__(self, bx_settings):
        self.bx_settings = bx_settings
        super(DefaultTokenStorage, self).__init__()

    def save_token(self, domain, token, refresh_token):
        storage = shelve.open(path.abspath(self.bx_settings.TOKEN_STORAGE_FILE_PATH))
        storage[domain] = {'token': token, 'refresh_token': refresh_token}
        storage.close()

    def get_client_credentials(self, domain):
        credentials = self.bx_settings.BX24_DOMAIN_SETTINGS[domain]
        return {
            'client_id': credentials['client_id'],
            'client_secret': credentials['client_secret']
        }

    def get_token(self, domain):
        # type: (str) -> str
        storage = shelve.open(self.bx_settings.TOKEN_STORAGE_FILENAME)
        result = storage[domain]['token']
        storage.close()
        return result

    def get_refresh_token(self, domain):
        # type: (str) -> str
        storage = shelve.open(self.bx_settings.TOKEN_STORAGE_FILENAME)
        result = storage[domain]['refresh_token']
        storage.close()
        return result

    def refresh_token(self, domain):
        # type: (str) -> str
        url = 'https://{}.bitrix24.ru/oauth/token/'.format(domain)
        domain_options = self.get_client_credentials(domain)
        params = {
            'client_id': domain_options['client_id'],
            'client_secret': domain_options['client_secret'],
            'grant_type': 'refresh_token',
            'refresh_token': self.get_refresh_token(domain)
        }
        response = requests.get(url, params)
        result = response.json()
        token, refresh_token = result['access_token'], result['refresh_token']
        self.save_token(domain, token, refresh_token)
        return token
