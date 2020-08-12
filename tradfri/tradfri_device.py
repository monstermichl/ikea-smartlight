import colorsys

from coap.coap import Coap
from config.config import Config
from tradfri.tradfri_endpoint import TradfriEndpoint
from common.helper import json_helper


def get_tradfri_devices(config: Config):
    devices_ids = Coap.get(config, TradfriEndpoint.DEVICE)
    devices     = []

    for device_id in devices_ids:
        # try if device is a color light bulb
        device = TradfriColorLightBulb.get_device(config, device_id)

        # if device is no color light bulb, try if it is a usual light bulb
        if device is None:
            device = TradfriLightBulb.get_device(config, device_id)

        # if device is no usual light bulb, try if it is a remote control
        if device is None:
            device = TradfriRemote.get_device(config, device_id)

        # if device is no remote control, just parse it as device
        if device is None:
            device = TradfriDevice.get_device(config, device_id)

        # if device has been parsed successfully, add it to the devices list
        if device is not None:
            devices.append(device)

    return devices


class TradfriProductInfo:
    __JSON_KEY_PRODUCT_INFO              = '3'
    __JSON_KEY_PRODUCT_INFO_DESCRIPTION  = '1'
    __JSON_KEY_PRODUCT_INFO_MANUFACTURER = '0'
    __JSON_KEY_PRODUCT_INFO_VERSION      = '3'

    def __init__(self, description, manufacturer, version):
        self.description  = description
        self.manufacturer = manufacturer
        self.version      = version

    @staticmethod
    def from_json(json):
        """ creates a TradfriProductInfo instance out of a valid TRADFRI coap-client JSON response """
        product_info = None

        try:
            json_temp = json_helper(json)

            product_info_entry = json_temp[TradfriProductInfo.__JSON_KEY_PRODUCT_INFO]
            product_info       = TradfriProductInfo(product_info_entry[TradfriProductInfo.__JSON_KEY_PRODUCT_INFO_DESCRIPTION ],
                                                    product_info_entry[TradfriProductInfo.__JSON_KEY_PRODUCT_INFO_MANUFACTURER],
                                                    product_info_entry[TradfriProductInfo.__JSON_KEY_PRODUCT_INFO_VERSION     ])

        except Exception as e:
            # neither valid JSON string nor JSON object
            pass

        return product_info


class TradfriDevice:
    __JSON_KEY_INSTANCE_ID   = '9003'
    __JSON_KEY_CREATION_DATE = '9002'
    __JSON_KEY_NAME          = '9001'

    def __init__(self, id, name, creation_date, product_info: TradfriProductInfo=None, api_config: Config=None):
        self.id            = id
        self.name          = name
        self.creation_date = creation_date
        self.product_info  = product_info
        self.api_config    = api_config

    @staticmethod
    def from_json(json, api_config: Config=None):
        """ creates a TradfriDevice instance out of a valid TRADFRI coap-client JSON response """
        device = None

        try:
            json_temp    = json_helper(json)
            product_info = TradfriProductInfo.from_json(json)

            device = TradfriDevice(json_temp[TradfriDevice.__JSON_KEY_INSTANCE_ID  ],
                                   json_temp[TradfriDevice.__JSON_KEY_NAME         ],
                                   json_temp[TradfriDevice.__JSON_KEY_CREATION_DATE], product_info, api_config)

        except Exception as e:
            # neither valid JSON string nor JSON object
            pass

        return device

    @staticmethod
    def get_device(config: Config, id):
        json = Coap.get(config, TradfriEndpoint.DEVICE, id)
        return TradfriDevice.from_json(json)


class TradfriLightBulb(TradfriDevice):
    __JSON_KEY_BULB                 = '3311'
    __JSON_KEY_BULB_STATE           = '5850'
    __JSON_KEY_BULB_BRIGHTNESS      = '5851'
    __JSON_KEY_BULB_COLOR           = '5706'
    __JSON_KEY_BULB_COLOR_X         = '5709'
    __JSON_KEY_BULB_COLOR_Y         = '5710'
    __JSON_KEY_BULB_TEMPERATURE     = '5711'
    __JSON_KEY_BULB_TRANSITION_TIME = '5712'

    __MAX_BRIGHTNESS = 255

    def __init__(self, id, name, brightness=0, color=0, status=False, creation_date=0, product_info: TradfriProductInfo=None, api_config: Config=None):
        super().__init__(id, name, creation_date, product_info, api_config)

        self.brightness        = brightness
        self.color             = color
        self.color_description = TradfriLightBulb._map_color_value(self.color)
        self.status            = status

    @staticmethod
    def from_json(json, api_config: Config=None):
        """ creates a TradfriLightBulb instance out of a valid TRADFRI coap-client JSON response """
        light_bulb = None

        try:
            json_temp = json_helper(json)
            device    = TradfriDevice.from_json(json_temp)

            light_bulb_entry = json_temp[TradfriLightBulb.__JSON_KEY_BULB][0]
            brightness       = round((light_bulb_entry[TradfriLightBulb.__JSON_KEY_BULB_BRIGHTNESS] / TradfriLightBulb.__MAX_BRIGHTNESS) * 100, 2)
            status           = light_bulb_entry[TradfriLightBulb.__JSON_KEY_BULB_STATE]

            if TradfriLightBulb.__JSON_KEY_BULB_COLOR in light_bulb_entry:
                color = light_bulb_entry[TradfriLightBulb.__JSON_KEY_BULB_COLOR]
            else:
                color = 'Standard'

            light_bulb = TradfriLightBulb(device.id, device.name, brightness, color, status, device.creation_date,
                                          device.product_info, api_config)

        except Exception as e:
            # neither valid JSON string nor JSON object
            pass

        return light_bulb

    @staticmethod
    def get_device(config: Config, id):
        json = Coap.get(config, TradfriEndpoint.DEVICE, id)
        return TradfriLightBulb.from_json(json)

    @staticmethod
    def _map_color_value(color_value):
        color_map =\
        {
            "f5faf6": "White",
            "f1e0b5": "Warm",
            "efd275": "Glow",
        }

        for value, description in color_map.items():
            if value == color_value:
                color_value = description
                break

        return color_value


class TradfriColorLightBulb(TradfriLightBulb):
    __JSON_KEY_BULB            = '3311'
    __JSON_KEY_BULB_HUE        = '5707'
    __JSON_KEY_BULB_SATURATION = '5708'

    __MAX_HUE        = 65536
    __MAX_SATURATION = 65536

    def __init__(self, id, name, hue=0, saturation=0, brightness=0, status=False, creation_date=0, product_info: TradfriProductInfo=None, api_config: Config=None):
        super().__init__(id, name, brightness, 0, status, creation_date, product_info, api_config)

        self.hue        = round(hue, 2)
        self.saturation = round(saturation, 2)

        r, g, b = colorsys.hsv_to_rgb(self.hue / 360, self.saturation / 100, self.brightness / 100)

        r *= 255
        g *= 255
        b *= 255

        self.color             = f'{int(r):02x}{int(g):02x}{int(b):02x}'
        self.color_description = TradfriColorLightBulb._map_color_value(self.color)

    @staticmethod
    def from_json(json, api_config: Config=None):
        """ creates a TradfriColorLightBulb instance out of a valid TRADFRI coap-client JSON response """
        color_light_bulb = None

        try:
            light_bulb = TradfriLightBulb.from_json(json)
            json_temp  = json_helper(json)

            color_light_bulb_entry = json_temp[TradfriColorLightBulb.__JSON_KEY_BULB][0]
            hue                    = (color_light_bulb_entry[TradfriColorLightBulb.__JSON_KEY_BULB_HUE] / TradfriColorLightBulb.__MAX_HUE) * 360
            saturation             = (color_light_bulb_entry[TradfriColorLightBulb.__JSON_KEY_BULB_SATURATION] / TradfriColorLightBulb.__MAX_SATURATION) * 100

            color_light_bulb = TradfriColorLightBulb(light_bulb.id           ,
                                                     light_bulb.name         ,
                                                     hue                     ,
                                                     saturation              ,
                                                     light_bulb.brightness   ,
                                                     light_bulb.status       ,
                                                     light_bulb.creation_date,
                                                     light_bulb.product_info ,
                                                     api_config              )

        except Exception as e:
            # neither valid JSON string nor JSON object
            pass

        return color_light_bulb

    @staticmethod
    def get_device(config: Config, id):
        json = Coap.get(config, TradfriEndpoint.DEVICE, id)
        return TradfriColorLightBulb.from_json(json)

    @staticmethod
    def _map_color_value(color_value):
        color_map =\
        {
            "4a418a": "Blue",
            "6c83ba": "Light Blue",
            "8f2686": "Saturated Purple",
            "a9d62b": "Lime",
            "c984bb": "Light Purple",
            "d6e44b": "Yellow",
            "d9337c": "Saturated Pink",
            "da5d41": "Dark Peach",
            "dc4b31": "Saturated Red",
            "dcf0f8": "Cold sky",
            "e491af": "Pink",
            "e57345": "Peach",
            "e78834": "Warm Amber",
            "e8bedd": "Light Pink",
            "eaf6fb": "Cool daylight",
            "ebb63e": "Candlelight",
            "efd275": "Warm glow",
            "f1e0b5": "Warm white",
            "f2eccf": "Sunrise",
            "f5faf6": "Cool white"
        }

        for value, description in color_map.items():
            if value == color_value:
                color_value = description
                break

        return color_value


class TradfriRemote(TradfriDevice):
    _JSON_KEY_SUB_LINKS = '15009'

    def __init__(self, id, name, creation_date=0, product_info: TradfriProductInfo=None, api_config: Config=None):
        super().__init__(id, name, creation_date, product_info, api_config)

    @staticmethod
    def from_json(json, api_config: Config=None):
        """ creates a TradfriRemote instance out of a valid TRADFRI coap-client JSON response """
        remote = None

        try:
            json_temp = json_helper(json)

            if TradfriRemote._JSON_KEY_SUB_LINKS in json_temp:
                device = TradfriDevice.from_json(json_temp)
                remote = TradfriRemote(device.id, device.name, device.creation_date, device.product_info, api_config)

        except Exception as e:
            # neither valid JSON string nor JSON object
            pass

        return remote

    @staticmethod
    def get_device(config: Config, id):
        json = Coap.get(config, TradfriEndpoint.DEVICE, id)
        return TradfriRemote.from_json(json)
