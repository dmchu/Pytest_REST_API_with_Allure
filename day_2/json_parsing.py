import json

def create_json_data():
    string_as_json_format = '{"answer": "Hello, Dude"}'
    obj = json.loads(string_as_json_format)
    return obj


