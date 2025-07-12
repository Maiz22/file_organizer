class DataType:
    """
    Class to group data by their endings.
    """
    def __init__(self, name:str, endings:dict) -> None:
        self.name = name
        self.endings = endings

    def __repr__(self) -> str:
        return f"Name: {self.name} - Ending: {self.endings}"