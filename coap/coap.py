import os
import sys
import json

from config.config import Config
from tradfri.endpoint import Endpoint


class Coap:
    __PATH_COAP_BIN = '/usr/local/bin/coap-client'
    __GET_TEMPLATE  = '{} -m get -u "{}" -k "{}" "{}" -B {} 2> /dev/null'
    __PUT_TEMPLATE  = '{} -m put -u "{}" -k "{}" -e \'{}\' "{}'
    __TIMEOUT       = 5

    @staticmethod
    def _execute(call):
        if os.path.exists(Coap.__PATH_COAP_BIN):
            result = os.popen(call)
        else:
            sys.stderr.write('[-] libcoap: could not find libcoap.\n')
            sys.exit(1)

        return json.loads(result.read().strip('\n').split('\n')[-1])

    @staticmethod
    def _build_tradri_hub(hubip, endpoint: Endpoint, id=None):
        url = f'coaps://{hubip}:5684/'

        if endpoint == Endpoint.DEVICE:
            url += '15001'
        elif endpoint == Endpoint.GROUP:
            url += '15004'

        if id is not None:
            url += f'/{id}'

        return url

    @staticmethod
    def put(payload, api_config: Config, endpoint: Endpoint, id=None):
        call = Coap.__PUT_TEMPLATE.format(Coap.__PATH_COAP_BIN, api_config.apiuser, api_config.apikey, payload,
                                          Coap._build_tradri_hub(api_config.hubip, endpoint, id))
        return Coap._execute(call)

    @staticmethod
    def get(api_config: Config, endpoint: Endpoint, id=None):
        call = Coap.__GET_TEMPLATE.format(Coap.__PATH_COAP_BIN, api_config.apiuser, api_config.apikey,
                                          Coap._build_tradri_hub(api_config.hubip, endpoint, id),
                                          Coap.__TIMEOUT)
        return Coap._execute(call)
