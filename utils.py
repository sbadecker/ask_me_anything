import json


def load_json(path):
    with open(path, "r") as f:
        json_object = json.load(f)
    return json_object


def save_json(json_obj, path):
    with open(path, "w") as f:
        json.dump(json_obj, f)
