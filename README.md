# bx24-orm
Обертка для [Bitrix24 API](https://dev.1c-bitrix.ru/rest_help/).

С помощью нее вы можете вместо:

```
import requests

token = get_token_function()  # get your Bitrix24 token

# prepare your parameters
params = {
    'id': lead_id,
    'auth': token
}

reponse = requests.get(your_domain_url+'crm.lead.get', params)

# check if request is OK
if response.status_code < 300:
    result = response.json()['result']
else:
    handle_errors(response)
```

сделать так:

```
from bx24_orm.entity.crm import BxLead
from bx24_orm.exceptions.code_exceptions import BxException

try:
    result = BxLead.get(lead_id)
except BxException as ex:
    handle_error(ex)  # your handling code
```

# Установка

Чтобы установить пакет:

```
pip install bx24-orm
```

# Начало работы

1. Для начала нужно создать файл конфигурации `bx24_settings.py`. 
    Рекомендую создать его в корне проекта.
    ```pythonstub
    TOKEN_STORAGE_FILE_PATH = 'bx24_tokens'  # путь до файла где хранятся токены приложения
    DEFAULT_DOMAIN = '{Ваш домен 3-го уровня}'
    DEFAULT_TRANSPORT = 'json' # xml пока не поддерживается
    BX24_DOMAIN_SETTINGS = {
        '{домен 3-го уровня}': {
            'client_id': '{ваш_client_id}',
            'client_secret': '{ваш_client_secret}'
        }
    }
    ```
2. Далее добавьте путь до файла настроек в переменную окружения:
    `BX24_SETTINGS_MODULE`
3. Получите токены для доступа к API. Для удобства можете воспользоваться скриптом командной строки:
        
    `> bx24_cmd get_tokens -c {ваш client_id} -s {ваш client_secret} -d {ваш домен 3-го уровня в битрикс}`
    
    Далее пройдите по ссылке, появившейся в скрипте. Если нужно авторизируйтесь в вашем Bitrix24. И скопируйте параметр code из url браузера и вставьте его в консоль.
    
4. Используя python консоль в вашем проекте выполните следующий код:

    ```
    from bx24_orm.core import token_storage
    token_storage.save_token('ваш домен 3-го уровня', 'access_token', 'refresh_token')
    ```
5. Готово! Пакет готов к использованию!

# Кастомизация ваших моделей

```pythonstub
from bx24_orm.enitiy.crm import BxDeal, BxLead, BxCompany, BxField


class Deal(BxDeal):
    custom_field = BxField('UF_CRM_1539088441')


class Lead(BxLead):
    custom_field = BxField('UF_CRM_1539088367')


class Company(BxCompany):
    custom_field = BxField('UF_CRM_1539088478')
```
__Стоит помнить:__
  Для экономии трафика при изменении моделей, они отслеживают какие поля изменились.
  Следовательно, чтобы изменить ссылочные типы данных модели, например телефон, нужно делать так:
  ```pythonstub
    lead = Lead.get(1)
    new_phone = lead.phone()
    new_phone[0]['VALUE'] = 'NEW_VALUE'
    lead.phone = new_phone
    lead.save() 
```
#Заключение
Если у вас возникнут вопросы, то не стесняйтесь написать мне на почту: dmitriilazukov@gmail.com

Также приветствуются Pull Request-ы.

