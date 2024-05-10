from model import PathModel, DataTypeModel, Model
from view import View
from controller import Controller


if __name__ == "__main__":
    path_model = Model(dir="data", file="path.json")
    data_type_model = Model(dir="data", file="data_type.json")
    view = View()
    controller = Controller(view, path_model, data_type_model)
    controller.run()