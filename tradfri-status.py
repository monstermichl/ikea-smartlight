#!/usr/bin/env python

# file        : tradfri-status.py
# purpose     : getting status from the Ikea tradfri smart lights
#
# author      : harald van der laan
# date        : 2017/11/01
# version     : v1.2.0
#
# changelog   :
# - v1.2.0      update for gateway 1.1.15 issues                        (harald)
# - v1.1.0      refactor for cleaner code                               (harald)
# - v1.0.0      initial concept                                         (harald)

"""
    tradfri-status.py - getting status of the Ikea Tradfri smart lights

    This module requires libcoap with dTLS compiled, at this moment there is no python coap module
    that supports coap with dTLS. see ../bin/README how to compile libcoap with dTLS support
"""

# pylint convention disablement:
# C0103 -> invalid-name
# C0200 -> consider-using-enumerate
# pylint: disable=C0200, C0103

from __future__ import print_function
from __future__ import unicode_literals

import sys
import time

from config import config
from tradfri import tradfriStatus
from tqdm import tqdm

def main():
    """ main function """

    hubip   = config.hubip
    apiuser = config.apiuser
    apikey  = config.apikey

    lightbulbs = []
    lightgroups = []

    print('[ ] Tradfri: acquiring all Tradfri devices, please wait ...')
    devices = tradfriStatus.tradfri_get_devices(hubip, apiuser, apikey)
    groups = tradfriStatus.tradfri_get_groups(hubip, apiuser, apikey)

    for deviceid in tqdm(range(len(devices)), desc='Tradfri devices', unit=' devices'):
        lightbulb = tradfriStatus.tradfri_get_lightbulb(hubip, apiuser, apikey,
                                                             str(devices[deviceid]))
        if lightbulb is not None:
            lightbulbs.append(lightbulb)

    # sometimes the request are to fast, the will decline the request (flood security)
    # in this case you could increse the sleep timer
    time.sleep(.5)

    for groupid in tqdm(range(len(groups)), desc='Tradfri groups', unit=' group'):
        lightgroups.append(tradfriStatus.tradfri_get_group(hubip, apiuser, apikey,
                                                          str(groups[groupid])))

    print('[+] Tradfri: device information gathered')
    print('===========================================================\n')
    for _ in range(len(lightbulbs)):
        try:
            bulb_string = 'bulb ID {0:<5}, name: {1: <35}, brightness: {2: >6}, color: {3: >16}, state: {4}'\
                .format(lightbulbs[_].id,
                        lightbulbs[_].name,
                        lightbulbs[_].brightness,
                        lightbulbs[_].color_description,
                        lightbulbs[_].status)

            print(bulb_string)

        except KeyError:
            # device is not a lightbulb but a remote control, dimmer or sensor
            pass

    print('\n')

    for _ in range(len(lightgroups)):
        if lightgroups[_]["5850"] == 0:
            group_string = 'group ID: {0:<5}, name: {1: <16}, state: off'.format(lightgroups[_]["9003"], lightgroups[_]["9001"])
        else:
            group_string = 'group ID: {0:<5}, name: {1: <16}, state: on'.format(lightgroups[_]["9003"], lightgroups[_]["9001"])

        print(group_string)

if __name__ == "__main__":
    main()
    sys.exit(0)
