from pydantic import BaseModel


class DataType(BaseModel):
    name: str
    endings: list = []
    path: str = ""
