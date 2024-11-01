import json
import os
import requests
from sys import argv


def load_json_file(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise Exception(f"File {file_path} not found.")


def save_json_file(file_path: str, data: dict):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def check_setting(settings_dict: dict, target_setting: str):
    for k, v in settings_dict.items():
        if k == target_setting:
            if type(v) != dict:
                return v
            else:
                if "default_value" in v:
                    return v.get("default_value")
                elif "value" in v:
                    return v.get("value")
                else:
                    return v
        elif type(v) == dict:
            new_setting = check_setting(v, target_setting)
            if new_setting:
                return new_setting
    return False


def parse_cura_dict(sample: dict, cura_dict: dict, new_dict: dict):
    for k, v in sample.items():
        if type(v) == dict:
            new_dict[k] = (parse_cura_dict(v, cura_dict, {}))
        else:
            new_setting = check_setting(cura_dict, v)
            if new_setting:
                new_dict[k] = new_setting
    return new_dict


def parse_cura_file(file_path: str):
    sample = load_json_file("snail-to-cura.json")
    cura_file = load_json_file(file_path)
    new_settings_dict = parse_cura_dict(sample, cura_file, {})
    return new_settings_dict

'''
def main(input_dir: str):
    url = "надо взять ссылку на сервис из константы"
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        output_setting_dict = parse_cura_file(file_path)
        response = requests.put(url, json=output_setting_dict)
        if response.status_code == 200:
            print(f"Successfully sent data from {file} to {url}")
        else:
            print(f"Failed to send data from {file} to {url}. Status code: {response.status_code}")

'''

if __name__ == "__main__":
    '''
    _, input_dir = argv
    main(input_dir)
    '''
    save_json_file("imported_ultimaker_original.def.json", parse_cura_file("ultimaker_original.def.json"))
