from pydantic import BaseModel


class DataType(BaseModel):
    """
    Model to represent a data type with its name and endings.
    """

    name: str
    endings: list[str]  # List of file endings, e.g., ['doc', 'docx', 'pdf']


class DataTypePathConfig(BaseModel):
    """
    Model representing data setup by combining data_type and
    target path.
    """

    data_type: DataType
    path: str
