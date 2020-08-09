import json


def json_helper(json_obj):
    if isinstance(json_obj, str):
        json_obj = json.loads(json_obj)
    return json_obj


class ProductInfo:
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
        """ creates a ProductInfo instance out of a valid TRADFRI coap-client JSON response """
        try:
            json_temp = json_helper(json)

            product_info_entry = json_temp[ProductInfo.__JSON_KEY_PRODUCT_INFO]
            product_info       = ProductInfo(product_info_entry[ProductInfo.__JSON_KEY_PRODUCT_INFO_DESCRIPTION ],
                                             product_info_entry[ProductInfo.__JSON_KEY_PRODUCT_INFO_MANUFACTURER],
                                             product_info_entry[ProductInfo.__JSON_KEY_PRODUCT_INFO_VERSION     ])

        except Exception as e:
            # neither valid JSON string nor JSON object
            raise e

        return product_info


class Device:
    __JSON_KEY_INSTANCE_ID   = '9003'
    __JSON_KEY_CREATION_DATE = '9002'
    __JSON_KEY_NAME          = '9001'

    def __init__(self, id, name, creation_date, product_info: ProductInfo=None):
        self.id            = id
        self.name          = name
        self.creation_date = creation_date
        self.product_info  = product_info

    def from_json(json):
        """ creates a Device instance out of a valid TRADFRI coap-client JSON response """
        try:
            json_temp    = json_helper(json)
            product_info = ProductInfo.from_json(json)

            device = Device(json_temp[Device.__JSON_KEY_INSTANCE_ID  ],
                            json_temp[Device.__JSON_KEY_NAME         ],
                            json_temp[Device.__JSON_KEY_CREATION_DATE], product_info)

        except Exception as e:
            # neither valid JSON string nor JSON object
            raise e

        return device


class LightBulb(Device):
    __JSON_KEY_BULB                 = '3311'
    __JSON_KEY_BULB_STATE           = '5850'
    __JSON_KEY_BULB_DIMMER          = '5851'
    __JSON_KEY_BULB_COLOR           = '5706'
    __JSON_KEY_BULB_COLOR_X         = '5709'
    __JSON_KEY_BULB_COLOR_Y         = '5710'
    __JSON_KEY_BULB_TEMPERATURE     = '5711'
    __JSON_KEY_BULB_TRANSITION_TIME = '5712'

    def __init__(self, id, name, brightness=0, color=0, status=False, creation_date=0, product_info: ProductInfo=None):
        super().__init__(id, name, creation_date, product_info)

        self.brightness        = brightness
        self.color             = color
        self.color_description = LightBulb._map_color_value(self.color)
        self.status            = status

    def from_json(json):
        """ creates a LightBulb instance out of a valid TRADFRI coap-client JSON response """
        try:
            json_temp = json_helper(json)
            device    = Device.from_json(json_temp)

            light_bulb_entry = json_temp[LightBulb.__JSON_KEY_BULB][0]
            brightness       = light_bulb_entry[LightBulb.__JSON_KEY_BULB_DIMMER]
            status           = light_bulb_entry[LightBulb.__JSON_KEY_BULB_STATE ]
            color            = light_bulb_entry[LightBulb.__JSON_KEY_BULB_COLOR ]

            light_bulb = LightBulb(device.id, device.name, brightness, color, status, device.creation_date, device.product_info)

        except Exception as e:
            # neither valid JSON string nor JSON object
            raise e

        return light_bulb

    @staticmethod
    def _map_color_value(color_value):
        color_map =\
        {
            "f5faf6": "White",
            "f1e0b5": "Warm",
            "efd275": "Glow",
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

        mapped_value = ''
        for value, description in color_map.items():
            if value == color_value:
                mapped_value = description
                break

        return mapped_value
