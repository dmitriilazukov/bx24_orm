# -*- coding: utf-8 -*-

from .token_storage import DefaultTokenStorage

BX_SETTINGS_MODULE = 'BX24_SETTINGS_MODULE'


class Bx24Settings(object):
    def __init__(self, settings_dict):
        self.TOKEN_STORAGE_FILENAME = 'bx24_tokens'
        self.TOKEN_STORAGE_CLS = DefaultTokenStorage
        for k in settings_dict:
            setattr(self, k, settings_dict[k])

    @property
    def default_domain(self):
        settings_default_domain = getattr(self, 'DEFAULT_DOMAIN', None)
        if not settings_default_domain:
            raise RuntimeError('Default domain not specified')
        return settings_default_domain

    @property
    def default_transport(self):
        return getattr(self, 'DEFAULT_TRANSPORT', 'json')
