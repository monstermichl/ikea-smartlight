from coap.coap import Coap
from config.config import Config
from tradfri.tradfri_endpoint import TradfriEndpoint
from common.helper import json_helper


def get_tradfri_groups(config: Config):
    group_ids = Coap.get(config, TradfriEndpoint.GROUP)
    groups    = []

    for group_id in group_ids:
        # try if group can be parsed
        group = TradfriGroup.get_group(config, group_id)

        # if group has been parsed successfully, add it to the groups list
        if group is not None:
            groups.append(group)

    return groups


class TradfriGroup:
    __JSON_KEY_INSTANCE_ID     = '9003'
    __JSON_KEY_CREATION_DATE   = '9002'
    __JSON_KEY_NAME            = '9001'
    __JSON_KEY_REMOTES         = '9018'
    __JSON_KEY_REMOTE_ENDPOINT = '15002'
    __JSON_KEY_STATE           = '5850'
    __JSON_KEY_BRIGHTNESS      = '5851'
    __JSON_KEY_SCENE_ID        = '9039'

    def __init__(self, id, name, creation_date, state, brightness, device_ids: [], api_config: Config=None):
        self.id            = id
        self.name          = name
        self.creation_date = creation_date
        self.state         = state
        self.brightness    = brightness
        self.device_ids    = device_ids
        self.api_config    = api_config

    @staticmethod
    def from_json(json, api_config: Config=None):
        """ creates a TradfriGroup instance out of a valid TRADFRI coap-client JSON response """
        device = None

        try:
            json_temp  = json_helper(json)
            device_ids = json_temp[TradfriGroup.__JSON_KEY_REMOTES][TradfriGroup.__JSON_KEY_REMOTE_ENDPOINT][TradfriGroup.__JSON_KEY_INSTANCE_ID]

            device = TradfriGroup(json_temp[TradfriGroup.__JSON_KEY_INSTANCE_ID  ],
                                  json_temp[TradfriGroup.__JSON_KEY_NAME         ],
                                  json_temp[TradfriGroup.__JSON_KEY_CREATION_DATE],
                                  json_temp[TradfriGroup.__JSON_KEY_STATE        ],
                                  json_temp[TradfriGroup.__JSON_KEY_BRIGHTNESS   ],
                                  device_ids                                      ,
                                  api_config                                      )

        except Exception as e:
            # neither valid JSON string nor JSON object
            pass

        return device

    @staticmethod
    def get_group(config: Config, id):
        json = Coap.get(config, TradfriEndpoint.GROUP, id)
        return TradfriGroup.from_json(json)
