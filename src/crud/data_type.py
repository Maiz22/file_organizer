from __future__ import annotations
from typing import TYPE_CHECKING
import json
import os
from config import DATA_TYPE_JSON_PATH
from model import DataType


def get_data_type_by_name(name: str) -> DataType:
    if os.path.exists(DATA_TYPE_JSON_PATH):
        with open(DATA_TYPE_JSON_PATH, "r") as json_file:
            try:
                data_type = json.load(json_file)[name]
                return DataType(**data_type)
            except KeyError:
                return None
    return None


def get_all_data_types() -> list[DataType]:
    try:
        with open(DATA_TYPE_JSON_PATH, "r") as json_file:
            data_types = json.load(json_file)
            return [DataType(**data) for data in data_types.values()]
    except FileNotFoundError:
        return []


def insert_data_type(data_type: DataType) -> None:
    try:
        with open(DATA_TYPE_JSON_PATH, "r") as json_file:
            data = json.load(json_file)
            data[data_type.name] = data_type.model_dump()
            with open(DATA_TYPE_JSON_PATH, "w") as json_file:
                json_file.write(json.dumps(data, indent=4))
    except FileNotFoundError:
        data = {data_type.name: data_type.model_dump()}
        with open(DATA_TYPE_JSON_PATH, "w") as json_file:
            json_file.write(json.dumps(data, indent=4))


def delete_data_type_by_name(name: str) -> bool:
    data = get_all_data_types()
    if name in data:
        data.pop(name)
        with open(DATA_TYPE_JSON_PATH, "w") as json_file:
            json_file.write(json.dumps(data, indent=4))
        return True
    return False


def delete_all_data_types() -> bool:
    data = {}
    try:
        with open(DATA_TYPE_JSON_PATH, "w") as json_file:
            json_file.write(json.dumps(data, indent=4))
            return True
    except FileNotFoundError:
        return False


def update_data_type(name: str, data_type: DataType) -> bool:
    """
    Update an existing data type in the JSON file.
    """
    if not name or not data_type:
        return False
    try:
        with open(DATA_TYPE_JSON_PATH, "r") as json_file:
            data = json.load(json_file)
            if name in data:
                data[name] = data_type.model_dump()
                with open(DATA_TYPE_JSON_PATH, "w") as json_file:
                    json_file.write(json.dumps(data, indent=4))
    except FileNotFoundError:
        return False
    return True
