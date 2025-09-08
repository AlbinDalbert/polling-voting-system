import json
import os

DATA_FILE = 'data.json'

def load_data():
    """Loads polls from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {"polls": {}}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    """Saves polls to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def log_action(action, message):
    pass
