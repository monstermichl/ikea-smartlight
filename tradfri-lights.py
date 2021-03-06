#!/usr/bin/env python

# file        : tradfri-lights.py
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
    tradfri-lights.py - controlling the Ikea tradfri smart lights

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
import argparse

from config.config import Config
from tradfri import tradfriActions
from tradfri.tradfri_device import TradfriLightBulb


def parse_args():
    """ function for getting parsed arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', choices=['power', 'brightness', 'color'], required=True)
    parser.add_argument('-l', '--lightbulbid', help='lightbulbid got from tradfri-status.py',
                        required=True)
    parser.add_argument('-v', '--value',
                        help='power: on/off, brightness: 0-100, color: warm/normal/cold',
                        required=True)

    args = parser.parse_args()

    return args


def main():
    """ main function """
    args = parse_args()

    config  = Config.get_default_config()
    hubip   = config.hubip
    apiuser = config.apiuser
    apikey  = config.apikey

    if args.action == 'power':
        TradfriLightBulb.set_power_static(args.lightbulbid, True if args.value == 'on' else False, config)
    elif args.action == 'brightness':
        if 1 <= int(args.value) <= 100:
            tradfriActions.tradfri_dim_light(hubip, apiuser, apikey, args.lightbulbid, args.value)
        else:
            sys.stderr.write('[-] Tradfri: dim value can only be between 1 and 100\n')
            sys.exit(1)
    elif args.action == 'color':
        if args.value == 'warm' or args.value == 'normal' or args.value == 'cold':
            tradfriActions.tradfri_color_light(hubip, apiuser, apikey, args.lightbulbid, args.value)
        else:
            sys.stderr.write('[-] Tradfri: color value can only be warm/normal/cold\n')
            sys.exit(1)


if __name__ == "__main__":
    main()
    sys.exit(0)
