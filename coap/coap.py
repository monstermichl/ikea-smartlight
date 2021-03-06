import os
import sys
import json

from config.config import Config
from tradfri.tradfri_endpoint import TradfriEndpoint


class Coap:
    __PATH_COAP_BIN = '/usr/local/bin/coap-client'
    __GET_TEMPLATE  = '{} -m get -u "{}" -k "{}" "{}" -B {} 2> /dev/null'
    __PUT_TEMPLATE  = '{} -m put -u "{}" -k "{}" -e \'{}\' "{}"'
    __TIMEOUT       = 5

    @staticmethod
    def _execute(call, return_json: bool=True):
        if os.path.exists(Coap.__PATH_COAP_BIN):
            result = os.popen(call)
        else:
            sys.stderr.write('[-] libcoap: could not find libcoap.\n')
            sys.exit(1)

        received_data = result.read()

        if return_json:
            result = json.loads(received_data.strip('\n').split('\n')[-1])

        return result

    @staticmethod
    def _build_tradri_hub(hubip, endpoint: TradfriEndpoint, id=None):
        url = f'coaps://{hubip}:5684/'

        if endpoint == TradfriEndpoint.DEVICE:
            url += '15001'
        elif endpoint == TradfriEndpoint.GROUP:
            url += '15004'

        if id is not None:
            url += f'/{id}'

        return url

    @staticmethod
    def put(payload, api_config: Config, endpoint: TradfriEndpoint, id=None, return_json: bool=True):
        call = Coap.__PUT_TEMPLATE.format(Coap.__PATH_COAP_BIN, api_config.apiuser, api_config.apikey, payload,
                                          Coap._build_tradri_hub(api_config.hubip, endpoint, id))

        return Coap._execute(call, return_json)

    @staticmethod
    def get(api_config: Config, endpoint: TradfriEndpoint, id=None):
        call = Coap.__GET_TEMPLATE.format(Coap.__PATH_COAP_BIN, api_config.apiuser, api_config.apikey,
                                          Coap._build_tradri_hub(api_config.hubip, endpoint, id),
                                          Coap.__TIMEOUT)
        return Coap._execute(call)
