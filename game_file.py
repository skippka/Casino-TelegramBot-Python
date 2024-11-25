import json

def read_from_file():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'balance': 1000, 'gameplay': 0}

def write_in_file(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
