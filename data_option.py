class DataOption:
    def __init__(self, name:str, path:str, file_format:dict) -> None:
        self.name = name
        self.path = path
        self.file_format = file_format
        self.data_list = []

    def __repr__(self) -> str:
        return f"{self.name} - {self.path} - {self.file_format}"