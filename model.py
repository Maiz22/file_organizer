#interaction with paths json or txt file
import os
import json


class Model():
    def __init__(self):
        self.dir = 'userdata'
        self.file = 'data.json'
        self.path = os.path.join(self.dir, self.file)
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        

    def get_path(self, name):
        if os.path.exists(self.path):
            with open(self.path, 'r') as json_file:
                try:
                    return json.load(json_file)[name]
                except KeyError:
                    return None

    def save_path(self, name, path):
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



if __name__ == "__main__":
    model = Model()