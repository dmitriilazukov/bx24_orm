# -*- coding: utf-8 -*-

import requests
import six
import argparse


def __get_tokens(client_id, client_secret, domain):
    code_url = 'https://{}.bitrix24.ru/oauth/authorize/?response_type=code&client_id={}'.format(domain, client_id)
    print(code_url)
    input_func = input
    if six.PY2:
        input_func = raw_input
    code = input_func('Follow link and copy code from result url. Then enter code here: ')
    auth_url = 'https://{}.bitrix24.ru/oauth/token/'.format(domain)
    auth_parameters = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'scope': ''
    }
    response = requests.get(auth_url, auth_parameters)
    if response.status_code == 200:
        result = response.json()
        auth_data = {
            'access_token': result['access_token'],
            'refresh_token': result['refresh_token']
        }
        print(auth_data)
        return 0
    else:
        print('Response status code {}. Try again!'.format(response.status_code))
        return -1


def bx24_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='[get_tokens]', action='store')
    parser.add_argument('-c', dest='client_id', help='client_id', action='store', type=str, required=True)
    parser.add_argument('-s', dest='client_secret', help='client_secret', action='store', type=str, required=True)
    parser.add_argument('-d', dest='domain', help='domain', action='store', type=str, required=True)
    parsed = parser.parse_args()
    if parsed.command == 'get_tokens':
        return __get_tokens(parsed.client_id, parsed.client_secret, parsed.domain)


if __name__ == '__main__':
    bx24_cmd()
