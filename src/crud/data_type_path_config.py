from __future__ import annotations
from typing import TYPE_CHECKING
import json
import os
from config import DATA_TYPE_DIRS_JSON_PATH

if TYPE_CHECKING:
    from model import DataTypePathConfig


def get_data_dirs_type_by_name(name: str) -> DataTypePathConfig:
    if os.path.exists(DATA_TYPE_DIRS_JSON_PATH):
        with open(DATA_TYPE_DIRS_JSON_PATH, "r") as json_file:
            try:
                data_type_dir = json.load(json_file)[name]
                return DataTypePathConfig(**data_type_dir)
            except KeyError:
                return None
    return None


def get_all_data_type_dirs() -> list[DataTypePathConfig]:
    try:
        with open(DATA_TYPE_DIRS_JSON_PATH, "r") as json_file:
            data_type_dirs = json.load(json_file)
            return [DataTypePathConfig(**data) for data in data_type_dirs.values()]
    except FileNotFoundError:
        return []


def insert_data_type_dir(name: str, data_type: DataTypePathConfig) -> None:
    try:
        with open(DATA_TYPE_DIRS_JSON_PATH, "r") as json_file:
            data = json.load(json_file)
            data[name] = data_type.model_dump()
            with open(DATA_TYPE_DIRS_JSON_PATH, "w") as json_file:
                json_file.write(json.dumps(data, indent=4))
    except FileNotFoundError:
        data = {name: data_type.model_dump()}
        with open(DATA_TYPE_DIRS_JSON_PATH, "w") as json_file:
            json_file.write(json.dumps(data, indent=4))


def delete_data_type_dir_by_name(name: str) -> bool:
    data = get_all_data_type_dirs()
    if name in data:
        data.pop(name)
        with open(DATA_TYPE_DIRS_JSON_PATH, "w") as json_file:
            json_file.write(json.dumps(data, indent=4))
        return True
    return False


def delete_all_data_types_dirs() -> bool:
    data = {}
    try:
        with open(DATA_TYPE_DIRS_JSON_PATH, "w") as json_file:
            json_file.write(json.dumps(data, indent=4))
    except FileNotFoundError:
        return False
    return


def update_data_type_dir(name: str, data_type_dir: DataTypePathConfig) -> bool:
    try:
        with open(DATA_TYPE_DIRS_JSON_PATH, "r") as json_file:
            data = json.load(json_file)
            if name in data:
                data[name] = data_type_dir.model_dump()
                with open(DATA_TYPE_DIRS_JSON_PATH, "w") as json_file:
                    json_file.write(json.dumps(data, indent=4))
    except FileNotFoundError:
        return False
    return True
