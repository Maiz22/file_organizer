#functional imports
from view import View
from model import Model
from default_data.data_formats import *
from data_type import DataType
from data_setup import DataSetup
import os

#imports to declare parameter types
from widgets.select_opiton import SelectOption
from widgets.setup_option import SetupOptionPopup


class Controller():
    def __init__(self, view: View, path_model:Model, data_type_model:Model) -> None:
        self.view = view
        self.path_model = path_model
        self.data_type_model = data_type_model
        #self.reset_default_data()
        self.data_types, self.data_setups = self.load_data_from_json()
        self.create_widgets()
        self.init_binds()

    def init_binds(self) -> None:
        """
        Bind the view's buttons to controllers methods.
        """
        self.view.add_btn_on_click(self.create_new_setup)
        self.view.check_btn_on_click(self.analyze_data)
        self.view.move_btn_on_click(self.move_data)
        self.view.default_btn_on_click(self.reset_to_default)

    def reset_to_default(self, event) -> None:
        """
        Resets all jsons to the default values, updates all
        widgets.
        """
        self.reset_default_data()
        self.data_types, self.data_setups = self.load_data_from_json()
        for child in self.view.target_path_frame.winfo_children():
            child.destroy()
        for child in self.view.base_path_frame.winfo_children():
            child.destroy()
        for child in self.view.result_frame.winfo_children():
            child.destroy()
        self.create_widgets()

    def set_default_setup(self) -> None:
        """
        Resets the path.json file to default (empty paths).
        """
        self.path_model.delete_all()
        self.path_model.insert_element(name="Base-Path", element="")
        for key in DEFAULT_DATA_FORMATS:
            self.path_model.insert_element(name=key, element="")

    def set_default_data_types(self) -> None:
        """
        Restes the data_type.json file to default values that
        are stored in DEFAULT_DATA_FORMATS.
        """
        self.data_type_model.delete_all()
        for key, data in DEFAULT_DATA_FORMATS.items():
            self.data_type_model.insert_element(name=key, element=list(data))

    def load_data_from_json(self) -> tuple[list, list]:
        """
        Get all elements from path.json and data_type.json.
        Creates DataType and DataSetup instance.
        """
        data_setups = []
        data_types = []
        paths = self.path_model.get_all()
        data_types_json = self.data_type_model.get_all()
        for key, val in data_types_json.items():
            data_type = DataType(name=key, endings=set(val))
            data_types.append(data_type)
            for path_key, path_val in paths.items():
                if path_key == data_type.name: 
                    data_setups.append(DataSetup(path=path_val, data_type=data_type))
        return data_types, data_setups

    def get_path_from_setup(self, name:str) -> str:
        """
        Takes a data type name as str and returns the corresponding
        path from the setup.
        """
        for setup in self.data_setups:
            if name.lower() == setup.data_type.name.lower():
                return setup.path

    def reset_default_data(self) -> None:
        """
        Reset all .json data.
        """
        self.set_default_setup()
        self.set_default_data_types()

    def create_widgets(self) -> None:
        """
        Create all default path widgets.
        """
        self.create_base_view()
        for setup in self.data_setups:
            if setup.data_type.name != "base-path":
                self.update_setup_view(setup)

    def create_base_view(self) -> None:
        self.view.create_select_path_widget(root=self.view.base_path_frame, label="Base-Path", 
                                    directory=self.get_path_from_setup("base-path"), 
                                    edit_callback=self.edit_base_path, 
                                    delete_callback=None,
                                    cancel=False)

    def edit_base_path(self, event, name:str) -> None:
        if name.lower() != "base-path":
            raise ValueError
        path = self.view.set_dir()
        self.path_model.update_element(name, path)
        for i, setup in enumerate(self.data_setups):
            if setup.data_type.name.lower() == name.lower():
                self.data_setups.pop(i)
        data_type = DataType(name, endings="")
        self.data_type_model.update_element(data_type.name, data_type.endings)
        self.data_types.append(data_type)
        self.data_setups.append(DataSetup(path=path, data_type=data_type))
        self.update_base_view()

    #def update_data_type(self, name, endings) -> None:
    #    try:
    #        self.data_type_model.delete_element(name)
    #    except KeyError:
    #        pass
    #    self.data_type_model.insert_element(name, element=endings)
#
#
    #def update_path(self, name, path) -> None:
    #    try:
    #        self.path_model.delete_element(name)
    #    except KeyError:
    #        pass
    #    self.path_model.insert_element(name, element=path)

    def update_base_view(self) -> None:
        for child in self.view.base_path_frame.winfo_children():
            child.destroy()
        self.create_base_view()
                
    def update_setup_view(self, setup:DataSetup) -> None:
        self.view.create_select_path_widget(root=self.view.target_path_frame, 
                        label=setup.data_type.name, 
                        directory=setup.path, 
                        edit_callback=self.edit_setup,
                        delete_callback=self.delete_setup,
                        cancel=True,
                        tip=f"{setup.data_type.endings}")
        
    def delete_setup(self, event, name) -> None:
        for i, setup in enumerate(self.data_setups):
            if setup.data_type.name == name:
                self.data_setups.pop(i)
        self.path_model.delete_element(name)
        self.data_type_model.delete_element(name)

                
    def edit_setup(self, event, name:str) -> None:
        """
        Takes the name of a setup and opens a prefilled
        edit setup view.
        """
        for setup in self.data_setups:
            if setup.data_type.name == name:
                edit_setup = self.view.edit_setup(setup)
        edit_setup.save_btn_on_click()

    def create_new_setup(self, event) -> None:
        """
        Opens a new setup popup and binds the save method
        to it.
        """
        new_setup = self.view.create_new_setup()
        new_setup.save_btn_on_click(lambda event=event, new_setup=new_setup: self.save_data_setup(event, new_setup))

    def save_edit_setup(self, event, new_option:SetupOptionPopup) -> None:
        pass

    def save_data_setup(self, event, new_option:SetupOptionPopup) -> None:
        data_type, data_setup = self.validate_data(new_option)
        if data_type and data_setup:
            self.data_type_model.insert_element(name=data_type.name, element=list(data_type.endings))
            self.path_model.insert_element(name=data_type.name, element=data_setup.path)
            self.data_types.append(data_type)
            self.data_setups.append(data_setup)
            self.update_setup_view(setup=data_setup)
            new_option.destroy()

    def validate_data(self, new_option:SetupOptionPopup) -> tuple[DataType|DataSetup]:
        """
        Validates data of te SetupOptionPopup and returns it
        if validation is successfull.
        """
        file_formats = {ending for ending in new_option.file_format_entry.get().split(",")}
        name=new_option.name_entry.get()
        try:
            data_type = self.validate_data_type(name=name, endings=file_formats)
        except ValueError:
            self.view.error_data_type_already_exists(f"'{name.lower()}'", new_option)
            return None, None
        try:
            data_setup = self.validate_data_setup(path=new_option.dir, data_type=data_type)
        except ValueError:
            self.view.info_enter_a_path(new_option)
            return None, None
        return (data_type, data_setup)

    def validate_data_type(self, name:str, endings:str) -> DataType|None:
        for data in self.data_types:
            if data.name.lower() == name.lower():
                raise ValueError("Datatype already exists.")
        return DataType(name=name, endings=endings)
    
    def validate_data_setup(self, path:str, data_type:DataType) -> DataSetup|None:
        if path is None:
            raise ValueError("Please enter a path.")
        return DataSetup(path=path, data_type=data_type)

    def load_setup(self) -> None:
        pass

    def save_dir(self, event, name:str, view_element:SelectOption) -> str:
        """
        Safe a path for the selected categgory to the user data json.
        """
        path = self.view.set_dir(name)
        if path:
            view_element.dir.configure(text=path)
            self.model.save_path(name=name, path=path)
        return "break" #return to reset button appearance

    def analyze_data(self, event) -> None:
        """
        Analize the data in the cleanup path.
        """
        self.clear_data()
        if self.model.get_setup("cleanup"):
            files = os.listdir(self.model.get_setup("cleanup"))
            for element in files:
                self.sort_data(data=element)
            self.display_findings()
        else:
            self.save_dir(event, name="cleanup", view_element=self.view.cleanup)

    def display_findings(self) -> None:
        """
        Show all findings from the cleanup path.
        """
        self.view.clear_result_frame()
        total_known = 0
        total_unknown = 0
        for data_category in self.data_type_categories:
            if data_category.list:
                self.view.display_results(label=data_category.name, amount=len(data_category.list), path=self.model.get_setup("cleanup"))#row=row,
                total_known += 1
            else:
                total_unknown += 1
        self.view.display_results(label="undefined data types", amount=total_unknown, path=self.model.get_setup("cleanup"))
        if total_known == 0 and total_unknown == 0:
            self.view.display_results(label="elements", amount=0, path=self.model.get_setup("cleanup"))#row=row,
        if total_known > 0:
            self.view.move_button.configure(state="enabled")

    def move_data(self, event) -> None:
        """
        Move the data from cleanup dir to the selected dirs depending
        on its data category.
        """
        for data_category in self.data_type_categories:
            for data in data_category.list:
                if self.model.get_setup(data_category.name):
                    os.replace(os.path.join(self.model.get_setup("cleanup"), data.name), os.path.join(self.model.get_setup(data_category.name), data.name))
                else:
                    self.save_dir(event, name=data_category.name, view_element=self.view.documents)
        self.update_bottom_view(event)

    def update_bottom_view(self, event) -> None:
        """
        Update the view displaying the data check results.
        """
        self.view.move_button.configure(state="disabled")

    def sort_data(self, data) -> None:
        """
        Sort the found data by data category ending and add it to 
        the corresponding data category list.
        """
        datatype = DataType(name=data, ending=data.split(".")[-1])
        for data_category in self.data_type_categories:
            if datatype.ending in data_category.endings:
                data_category.list.append(datatype)
            #else: self.other.list.append(datatype)

    def clear_data(self) -> None:
        """
        Clear all lists of the data category instances.
        """
        for data in self.data_type_categories:
            data.list = []
        
    def run(self) -> None:
        """
        Start the view mainloop.
        """
        self.view.mainloop()