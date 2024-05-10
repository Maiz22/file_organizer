import os
import json


class PathModel:
    def __init__(self) -> None:
        self.dir = 'data'
        self.file = 'path.json'
        self.path = os.path.join(self.dir, self.file)
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

    def get_element(self, name:str) -> None:
        if os.path.exists(self.path):
            with open(self.path, 'r') as json_file:
                try:
                    return json.load(json_file)[name]
                except KeyError:
                    return None
                
    def insert_element(self, name:str, path:str) -> None:
        new_data = {name: path}
        if not os.path.exists(self.path):
            with open(self.path, 'w') as json_file:
                json_file.write(json.dumps(new_data, indent=4))
        else: 
            with open(self.path, 'r') as json_file:
                data = json.load(json_file)
                data[name] = path
                with open(self.path, 'w') as json_file:
                    json_file.write(json.dumps(data, indent=4))

    def get_all(self) -> None:
        try:
            with open(self.path, "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            pass

    def delete_element(self, name:str) -> None:
        data = self.get_all()
        data.pop(name)
        with open(self.path, 'w') as json_file:
            json_file.write(json.dumps(data, indent=4))

    def delete_all(self) -> None:
        data={}
        try:
            with open(self.path, 'w') as json_file:
                json_file.write(json.dumps(data, indent=4))
        except FileNotFoundError:
            return

class DataTypeModel:
    def __init__(self) -> None:
        self.dir = 'data'
        self.file = 'data_type.json'
        self.path = os.path.join(self.dir, self.file)
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

    def get_element(self, name:str) -> None:
        if os.path.exists(self.path):
            with open(self.path, 'r') as json_file:
                try:
                    return json.load(json_file)[name]
                except KeyError:
                    return None

    def insert_element(self, name:str, endings:list) -> None:
        try:
            with open(self.path, "r") as json_file:
                data = json.load(json_file)
                data[name] = endings
                with open(self.path, 'w') as json_file:
                    json_file.write(json.dumps(data, indent=4))
        except FileNotFoundError:
            data = {}
            data[name] = endings
            with open(self.path, 'w') as json_file:
                json_file.write(json.dumps(data, indent=4))

    def delete_element(self, name:str) -> None:
        data = self.get_all()
        data.pop(name)
        with open(self.path, 'w') as json_file:
            json_file.write(json.dumps(data, indent=4))

    def get_all(self) -> None|dict:
        try:
            with open(self.path, "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            pass

    def delete_all(self) -> None:
        data={}
        try:
            with open(self.path, 'w') as json_file:
                json_file.write(json.dumps(data, indent=4))
        except FileNotFoundError:
            return