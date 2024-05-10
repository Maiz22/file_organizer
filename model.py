import os
import json


class Model:
    def __init__(self, dir, file) -> None:
        self.dir = dir
        self.file = file
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
                
    def get_all(self) -> list:
        try:
            with open(self.path, "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            pass

    def insert_element(self, name:str, element:list) -> None:
        try:
            with open(self.path, "r") as json_file:
                data = json.load(json_file)
                data[name] = element
                with open(self.path, 'w') as json_file:
                    json_file.write(json.dumps(data, indent=4))
        except FileNotFoundError:
            data = {}
            data[name] = element
            with open(self.path, 'w') as json_file:
                json_file.write(json.dumps(data, indent=4))

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