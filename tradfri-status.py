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

from tradfri.tradfri_device import *
from tradfri.tradfri_group import *


def main():
    """ main function """
    config = Config.get_default_config()

    print('[ ] Tradfri: acquiring all Tradfri devices, please wait ...')
    devices = get_tradfri_devices(config)
    groups  = get_tradfri_groups(config)

    # sometimes the request are to fast, the will decline the request (flood security)
    # in this case you could increse the sleep timer
    time.sleep(.5)

    print('[+] Tradfri: device information gathered')
    print('===========================================================\n')

    for device in devices:
        if isinstance(device, TradfriLightBulb) or \
           isinstance(device, TradfriColorLightBulb):

            try:
                bulb_string = 'bulb ID {0:<5}, name: {1: <35}, brightness: {2: >6}%, color: {3: >16}, state: {4}'\
                    .format(device.id,
                            device.name,
                            device.brightness,
                            device.color_description,
                            device.status)

                print(bulb_string)

            except KeyError:
                # device is not a lightbulb but a remote control, dimmer or sensor
                pass

    print('\n')

    for group in groups:
        print('group ID: {0:<5}, name: {1: <16}, state: {2}'.format(group.id, group.name, group.state))


if __name__ == "__main__":
    main()
    sys.exit(0)
