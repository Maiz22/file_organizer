#import to declare parameter type
from data_type import DataType

class DataSetup:
    """
    Class to create a data setup to combine data_type and
    target path.
    """
    def __init__(self, path:str, data_type:DataType) -> None: #name:str, endings,
        self.data_type = data_type
        self.path = path
        self.result_list = []

    def __repr__(self) -> str:
        return f"{self.data_type.name} - {self.path} - {self.data_type.endings}"