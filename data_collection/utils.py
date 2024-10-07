import os
import json

def check_directory_file_exists(path: str, error_message : str) -> None:
    if not os.path.exists(path):
        raise FileNotFoundError(f'Error 404 - Not Found: {error_message}')

def save_data(data, path):
    with open(path, "w") as f:
        json.dump(data, f)

def load_data(path):
    with open(path, "r") as f:
        return json.load(f)

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
