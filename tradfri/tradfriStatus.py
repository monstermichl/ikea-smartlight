#!/usr/bin/env python

# file        : tradfri/tradfriStatus.py
# purpose     : getting status from the Ikea tradfri smart lights
#
# author      : harald van der laan
# date        : 2017/11/01
# version     : v1.2.0
#
# changelog   :
# - v1.2.0      update for new gateway 1.1.15 issues                    (harald)
# - v1.1.0      refactor for cleaner code                               (harald)
# - v1.0.0      initial concept                                         (harald)

"""
    tradfriStatus.py - module for getting status of the Ikea tradfri smart lights

    This module requires libcoap with dTLS compiled, at this moment there is no python coap module
    that supports coap with dTLS. see ../bin/README how to compile libcoap with dTLS support
"""

# pylint convention disablement:
# C0103 -> invalid-name
# pylint: disable=C0103

from tradfri.tradfri_device import *
from tradfri.tradfri_endpoint import TradfriEndpoint


def tradfri_get_groups(hubip, apiuser, apikey):
    """ function for getting tradfri groups """
    config = Config(hubip, apiuser, apikey)
    return Coap.get(config, TradfriEndpoint.GROUP)


def tradfri_get_group(hubip, apiuser, apikey, groupid):
    """ function for getting tradfri group information """
    config = Config(hubip, apiuser, apikey)
    return Coap.get(config, TradfriEndpoint.GROUP, groupid)
