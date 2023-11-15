import json


def pretty_print_json(json_data):
    json_formatted_str = json.dumps(json_data, indent=2)
    print(json_formatted_str)
