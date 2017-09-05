import hashlib
import json

import logging
import random

import requests

from django.conf import settings


logger = logging.getLogger('app')


class PaymentFacade:

    terminal_url = settings.PAYMENT_URL
    merchand = settings.MERCHAND_ID
    secret1 = settings.SECRET1
    secret2 = settings.SECRET2
    email = 'payment@normasound.ru'

    def get_terminal(self, amount, order_id):
        seq = list(map(str, [self.merchand, amount, self.secret1, order_id]))
        sign = self._get_sign(seq)
        params = dict(m=self.merchand, oa=amount, o=order_id, s=sign, em=self.email)
        return '/?'.join([self.terminal_url,
                         '&'.join(['{}={}'.format(k, v) for k, v in params.items()])])

    def check_sign(self, params):
        order_id = params.get('MERCHANT_ORDER_ID')
        amount = params.get('AMOUNT')
        sign = params.get('SIGN')
        seq = list(map(str, [self.merchand, amount, self.secret2, order_id]))
        system_sign = self._get_sign(seq)
        return (False, True)[system_sign == sign]

    @staticmethod
    def _get_sign(seq):
        line = ':'.join(str(key) for key in seq)
        return hashlib.md5(line.encode('utf-8')).hexdigest()


payment_facade = PaymentFacade()


class NormaBot:
    SEND_SUCCESS_URL, SEND_FAIL_URL, SEND_MESSAGE_URL = 'sendSuccessURL', 'sendFailUrl', 'sendMessageUrl'

    METHODS = {
        SEND_SUCCESS_URL: 'send/success/',
        SEND_FAIL_URL: 'send/fail/',
        SEND_MESSAGE_URL: 'send/message/'
    }

    GET, POST, PUT = 'get', 'post', 'put'

    def __init__(self):
        self.bot_url = settings.BOT_URL
        self.token = settings.NORMA_BOT_TOKEN

    def request(self, url, params=None, http_method=GET):
        content = {}
        params = params or {}
        headers = {'Authorization': '{}'.format(self.token)}
        absolute_url = self.bot_url + url
        response = {}

        if http_method == self.GET:
            response = requests.get(absolute_url, headers=headers, params=params)
        elif http_method == self.POST:
            headers['Content-Type'] = 'application/json'
            response = requests.post(absolute_url, headers=headers, json=params)
        elif http_method == self.PUT:
            headers['Content-Type'] = 'application/json'
            response = requests.put(absolute_url, headers=headers, json=params)
        else:
            assert 'Unsupported http method'

        try:
            content = json.loads(response.content.decode('utf-8'))
        except ValueError:
            logger.error('Invalid response content [{}]'.format(response.content.decode('utf-8')))

        return content

    def send_success(self, guest):
        params = {'enter_code': guest.enter_code, 'chat_id': guest.chat_id}
        url = self.METHODS.get(self.SEND_SUCCESS_URL)
        self.request(url, params=params, http_method=self.POST)

    def send_fail(self, guest):
        params = {'chat_id': guest.chat_id}
        url = self.METHODS.get(self.SEND_FAIL_URL)
        self.request(url, params=params, http_method=self.POST)


norma_bot = NormaBot()


def generate_code(length):
    alpha_num = '1234567890'

    result = ''
    for _ in range(length):
        result += random.choice(alpha_num)
    return result
