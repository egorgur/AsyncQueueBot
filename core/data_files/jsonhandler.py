import json

import os

absolute_path = os.path.dirname(__file__)
absolute_path = absolute_path.split("\\")
absolute_path = absolute_path[:-1]
absolute_path = '\\'.join(absolute_path)


def read_json(file_name: str) -> (list, dict):
    with open(absolute_path + '\\data_files\\' + file_name, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(file_name: str, data: (list, dict)) -> None:
    with open(absolute_path + '\\data_files\\' + file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
