from model import PathModel, DataTypeModel
from view import View
from controller import Controller


if __name__ == "__main__":
    path_model = PathModel()
    data_type_model = DataTypeModel()
    view = View()
    controller = Controller(view, path_model, data_type_model)
    controller.run()