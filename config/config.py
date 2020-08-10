import os
import configparser


class Config:
    def __init__(self, hubip, apiuser, apikey):
        self.hubip   = hubip
        self.apiuser = apiuser
        self.apikey  = apikey

    @staticmethod
    def get_default_config():
        conf = configparser.ConfigParser()
        script_dir = os.path.dirname(os.path.realpath(__file__))
        conf.read(script_dir + '/../tradfri.cfg')

        hubip   = conf.get('tradfri', 'hubip')
        apiuser = conf.get('tradfri', 'apiuser')
        apikey  = conf.get('tradfri', 'apikey')

        return Config(hubip, apiuser, apikey)
