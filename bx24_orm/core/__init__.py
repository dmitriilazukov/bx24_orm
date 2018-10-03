import os
from importlib import import_module

from bx24_orm.core.settings import Bx24Settings

BX_SETTINGS_MODULE = 'BX24_SETTINGS_MODULE'
try:
    __settings_module = import_module(os.environ[BX_SETTINGS_MODULE])
except KeyError:
    __settings_module = []

__module_dict_vars = {}
for attr in dir(__settings_module):
    if not attr.startswith('__'):
        __module_dict_vars.update({attr: getattr(__settings_module, attr)})

settings = Bx24Settings(__module_dict_vars)
token_storage = settings.TOKEN_STORAGE_CLS(settings)
