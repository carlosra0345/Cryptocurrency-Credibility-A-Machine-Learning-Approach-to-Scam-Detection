# utils.py
# Houses heper functions that are shared acorss data collection scripts

import os
import json

def save_data(data, path):
    with open(path, "w") as f:
        json.dump(data, f)

def load_data(path):
    with open(path, "r") as f:
        return json.load(f)

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
