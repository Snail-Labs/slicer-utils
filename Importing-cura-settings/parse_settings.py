import json
import os
import requests
import argparse


def find_target_in_settings_recursive(settings_dict: dict, target_setting: str):
    for k, v in settings_dict.items():
        if k == target_setting:
            if not isinstance(v, dict):
                return v
            if "default_value" in v:
                return v.get("default_value")
            if "value" in v:
                return v.get("value")
            return v
        elif isinstance(v, dict):
            new_setting = find_target_in_settings_recursive(v, target_setting)
            if new_setting:
                return new_setting


def parse_cura_dict(sample: dict, cura_dict: dict, new_dict: dict) -> dict:
    for k, v in sample.items():
        if isinstance(v, dict):
            new_dict[k] = parse_cura_dict(v, cura_dict, {})
        else:
            new_setting = find_target_in_settings_recursive(cura_dict, v)
            if new_setting:
                new_dict[k] = new_setting
    return new_dict


def parse_cura_file(file_path: str):
    with open("snail-to-cura.json", "r", encoding="utf-8") as f1:
        mapper = json.load(f1)
    with open(file_path, "r", encoding="utf-8") as f2:
        cura_file = json.load(f2)
    new_settings_dict = parse_cura_dict(mapper, cura_file, {})
    return new_settings_dict


'''
def main(input_dir: str):
    url = "надо взять ссылку на сервис из константы"
    for file in os.listdir(os.path.abspath(input_dir)):
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
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str)
    args = parser.parse_args()
    main(args.input_dir)
    '''
    with open("imported_ultimaker_original.def.json", "w", encoding="utf-8") as f:
        json.dump(parse_cura_file("ultimaker_original.def.json"), f, indent=4)
