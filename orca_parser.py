import json
import logging
import os

# import requests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def merge_dicts_recursive(*dicts: dict):
    merged = {}
    for dictionary in dicts:
        for key, value in dictionary.items():
            if (
                    key in merged
                    and isinstance(merged[key], dict)
                    and isinstance(value, dict)
            ):
                merged[key] = merge_dicts_recursive(merged[key], value)
            else:
                merged[key] = value
    logger.info("successfully merged settings dictionaries")
    return merged


def file_to_data(path: str) -> dict:
    try:
        with open(path, "r") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError("Data must be an instance of dict")
        return data
    except FileNotFoundError:
        logger.error(f"File {path} not found")
    except json.JSONDecodeError:
        logger.error(f"JSON decode error for {path}")
    return {}


def load_orca_configs(
        machine_file_path: str, process_file_path: str, filament_file_path: str
) -> dict:
    machine_data: dict = file_to_data(machine_file_path)
    process_data: dict = file_to_data(process_file_path)
    filament_data: dict = file_to_data(filament_file_path)

    main_settings: dict = merge_dicts_recursive(
        machine_data, process_data, filament_data
    )
    logger.info("successfully load configs")
    return main_settings


def check_setting_recursive(settings_dict: dict, target_setting: str):
    for k, v in settings_dict.items():
        if k == target_setting:
            if isinstance(v, list):
                return v[0]
            return v
        elif type(v) == dict:
            new_setting = check_setting_recursive(v, target_setting)
            if new_setting:
                return new_setting
    return


def parse_dict_recursive(sample: dict, orca_dict: dict, new_dict) -> dict:
    for k, v in sample.items():
        if isinstance(v, dict):
            new_dict[k] = parse_dict_recursive(v, orca_dict, {})
        else:
            new_setting = check_setting_recursive(orca_dict, v)
            if new_setting:
                new_dict[k] = new_setting
    return new_dict


def transform_process(
        machine_config_path: str, process_config_path: str, filament_config_path: str
) -> None | dict:
    sample_ = file_to_data(os.path.join("docs", "snail-to-orca.json"))
    main_settings_ = load_orca_configs(
        machine_config_path, process_config_path, filament_config_path
    )
    # main_settings_ = load_orca_configs('docs/example/fdm_machine_common.json', 'docs/example/fdm_process_common.json', 'docs/example/fdm_filament_common.json')
    if main_settings_:
        new_dict_ = parse_dict_recursive(
            sample=sample_, orca_dict=main_settings_, new_dict={}
        )
        logger.info("successfully transform settings")
        return new_dict_ if new_dict_ else None


"""
def main():
    URL = "url/to/validate/service"

    тут надо взять из директории три файла конфигов(machine, process, filament) и закинуть их в transform_process
    snail_settings_dict = transform_process(machine_config_path, process_config_path, filament_config_path)
    response = requests.put(URL, json=snail_settings_dict)
    if response.status_code == 200:
        logger.info('Successfully updated settings')
    logger.info('Error in process')
"""
