class DataTypeCategory:
    def __init__(self, name, endings):
        self.name = name
        self.endings = endings
        self.list = []

    def __repr__(self):
        return f"{self.name}: {self.list}"
    
class DataType:
    def __init__(self, name, ending):
        self.name = name
        self.ending = ending

    def __repr__(self):
        return f"Name: {self.name}\nEnding: {self.ending}"