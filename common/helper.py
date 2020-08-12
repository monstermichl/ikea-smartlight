import json


def json_helper(json_obj):
    if isinstance(json_obj, str):
        json_obj = json.loads(json_obj)
    return json_obj
