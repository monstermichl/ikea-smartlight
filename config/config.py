import os
import ConfigParser

hubip   = ''
apiuser = ''
apikey  = ''

def get_config():
    global hubip
    global apiuser
    global apikey

    conf = ConfigParser.ConfigParser()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    conf.read(script_dir + '/../tradfri.cfg')

    hubip   = conf.get('tradfri', 'hubip')
    apiuser = conf.get('tradfri', 'apiuser')
    apikey  = conf.get('tradfri', 'apikey')


get_config()
