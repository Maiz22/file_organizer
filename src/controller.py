#functional imports
from view import View
from model import Model
from default_data.data_formats import *
from data_type import DataType
from data_setup import DataSetup
import os

#imports to declare parameter types
from widgets.setup_option import SetupOptionPopup


class Controller():
    def __init__(self, view: View, path_model:Model, data_type_model:Model) -> None:
        self.view = view
        self.path_model = path_model
        self.data_type_model = data_type_model
        self.data_types, self.data_setups = self.load_data_from_json()
        self.update_all_setup_widgets()
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
        self.reset_path_db()
        self.reset_data_type_db()
        self.reset_all_widgets()

    def reset_all_widgets(self) -> None:
        self.data_types, self.data_setups = self.load_data_from_json()
        self.view.destroy_child_widgets(self.view.target_path_frame)
        self.view.destroy_child_widgets(self.view.base_path_frame)
        self.view.destroy_child_widgets(self.view.result_frame)
        self.update_all_setup_widgets()

    def reset_path_db(self) -> None:
        """
        Resets the path.json file to default (empty paths).
        """
        self.path_model.delete_all()
        self.path_model.insert_element(name="Base-Path", element="")
        for key in DEFAULT_DATA_FORMATS:
            self.path_model.insert_element(name=key, element="")

    def reset_data_type_db(self) -> None:
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
            data_type = DataType(name=key, endings=val)
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

    def update_all_setup_widgets(self) -> None:
        """
        Create all default path widgets.
        """
        self.create_base_widget()
        for setup in self.data_setups:
            if setup.data_type.name.lower() != "base-path":
                self.create_setup_widget(setup)

    def create_setup_widget(self, setup:DataSetup) -> None:
        """
        Helper function updating the setup widgets of the view.
        """
        self.view.create_select_path_widget(root=self.view.target_path_frame, 
                        label=setup.data_type.name, 
                        directory=setup.path, 
                        edit_callback=self.edit_setup,
                        delete_callback=self.delete_setup,
                        cancel=True,
                        tip=f"{setup.data_type.endings}")

    def update_base_view(self) -> None:
        """
        Destroy all widgets inside the base_path_frame and 
        call the create base view function.
        """
        for child in self.view.base_path_frame.winfo_children():
            child.destroy()
        self.create_base_widget()

    def create_base_widget(self) -> None:
        """
        Creates the base-path view inside the view instance.
        """
        self.view.create_select_path_widget(root=self.view.base_path_frame, label="Base-Path", 
                                    directory=self.get_path_from_setup("base-path"), 
                                    edit_callback=self.edit_base_path, 
                                    delete_callback=None,
                                    cancel=False)

    def edit_base_path(self, event, name:str) -> None:
        """
        Edits the base path by validating the chosen path, adding 
        it to the DBs and temp lists and updating the view.
        """
        path = self.view.set_dir()
        try:
            self.validate_base_path(name=name, path=path)
        except ValueError:
            return "break"
        self.path_model.update_element(name, path)
        self.remove_elements_from_temp_lists(name)
        data_type = DataType(name, endings="")
        self.data_type_model.update_element(data_type.name, data_type.endings)
        self.data_types.append(data_type)
        self.data_setups.append(DataSetup(path=path, data_type=data_type))
        self.update_base_view()
        return "break"
        
    def delete_setup(self, event, name) -> None:
        """
        Removing setups (path and datatype) for their 
        corrseponding DBs.
        """
        self.remove_elements_from_temp_lists(name)
        self.path_model.delete_element(name)
        self.data_type_model.delete_element(name)

    def remove_elements_from_temp_lists(self, name) -> None:
        """
        Helper function removing element name from the
        temp lists.
        """
        for i, setup in enumerate(self.data_setups):
            if setup.data_type.name == name:
                self.data_setups.pop(i)
        for i, data_type in enumerate(self.data_types):
            if data_type.name == name:
                self.data_types.pop(i)
        
    def edit_setup(self, event, name:str) -> None:
        """
        Takes the name of a setup and opens a prefilled
        edit setup view.
        """
        for setup in self.data_setups:
            if setup.data_type.name == name:
                edit_setup = self.view.edit_setup(setup)
        edit_setup.save_btn_on_click(lambda event=event, edit_setup=edit_setup, name=name: self.save_setup_data_edit(event, edit_setup, name))

    def save_setup_data_edit(self, event, edit_setup:SetupOptionPopup, name:str) -> None:
        """
        Save edited setup. Only validate the path, since the name
        cannot be changed in the frontend. Remove the old elements from
        temp lists and DBs and add the new once.
        """
        name = edit_setup.name_entry.get()
        new_endings = edit_setup.file_format_entry.get()
        endings = new_endings.split(",")
        path = edit_setup.dir
        data_type = DataType(name=name, endings=endings)
        try:
            data_setup = self.validate_setup_path(path=path, data_type=data_type)
        except ValueError:
            self.view.info_enter_a_path(edit_setup)
            return
        self.data_type_model.delete_element(name)
        self.data_type_model.insert_element(name, element=endings)
        self.path_model.delete_element(name)
        self.path_model.insert_element(name, element=path)
        self.remove_elements_from_temp_lists(name)
        self.data_types.append(data_type)
        self.data_setups.append(data_setup)
        self.reset_all_widgets()
        edit_setup.destroy()

    def create_new_setup(self, event) -> None:
        """
        Opens a new setup popup and binds the save method
        to it.
        """
        new_setup = self.view.create_new_setup()
        new_setup.save_btn_on_click(lambda event=event, new_setup=new_setup: self.save_setup_data(event, new_setup))

    def save_setup_data(self, event, new_option:SetupOptionPopup) -> None:
        """
        Validates the newly created data, adds it in to the temp data/setup lists
        and adds it to the DBs.
        """
        data_type, data_setup = self.validate_new_data(new_option)
        if data_type and data_setup:
            self.data_type_model.insert_element(name=data_type.name, element=list(data_type.endings))
            self.path_model.insert_element(name=data_type.name, element=data_setup.path)
            self.data_types.append(data_type)
            self.data_setups.append(data_setup)
            self.create_setup_widget(setup=data_setup)
            new_option.destroy()

    def validate_new_data(self, new_option:SetupOptionPopup) -> tuple[DataType|DataSetup]:
        """
        Validates data of te SetupOptionPopup and returns it
        if validation is successfull.
        """
        file_formats = {ending for ending in new_option.file_format_entry.get().split(",")}
        name=new_option.name_entry.get()
        try:
            data_type = self.validate_data_type(name=name, endings=file_formats)
        except ValueError:
            self.view.error_invalid_data_type_name(f"'{name.lower()}'", new_option)
            return None, None
        try:
            data_setup = self.validate_setup_path(path=new_option.dir, data_type=data_type)
        except ValueError:
            self.view.info_enter_a_path(new_option)
            return None, None
        return (data_type, data_setup)

    def validate_data_type(self, name:str, endings:str) -> DataType|None:
        """
        Check whether an element already exists in the DB. 
        """
        for data in self.data_types:
            if name == "" or data.name.lower() == name.lower():
                raise ValueError("Datatype already exists.")
        return DataType(name=name, endings=endings)
    
    def validate_setup_path(self, path:str, data_type:DataType) -> DataSetup|None:
        """
        Checks if a path has been added to a new setup.
        """
        if path is None or path == "":
            raise ValueError("Please enter a path.")
        return DataSetup(path=path, data_type=data_type)
    
    def validate_base_path(self, name, path):
        """
        Checks if path is not emptry and base-path is selceted.
        """
        if name.lower() != "base-path" or path == "":
            raise ValueError("Invalid base path!")

    def analyze_data(self, event) -> None:
        """
        Analize the data in the cleanup path.
        """

        self.sorted_dict = self.create_sorting_dictionary()
        path = self.path_model.get_element("Base-Path")
        if path != "":
            files = os.listdir(path)
            for element in files:
                self.sort_data(data=element)
        else:
            self.view.info_select_base_dir()
        self.display_findings()

    def create_sorting_dictionary(self) -> dict:
        sort_dict = {"unknown": []}
        for data_type in self.data_types:
            sort_dict[data_type.name] = []
        return sort_dict

    def display_findings(self) -> None:
        """
        Show all findings from the cleanup path.
        """
        check_move = False
        base_path = self.get_path_from_setup(name="Base-Path")
        self.view.destroy_child_widgets(self.view.result_frame)
        for data in self.data_types:
            if self.sorted_dict[data.name]:
                self.view.display_results(label=data.name, amount=len(self.sorted_dict[data.name]), path=base_path)
                check_move = True
        if self.sorted_dict["unknown"]:
            self.view.display_results(label="undefined data types", amount=len(self.sorted_dict["unknown"]), path=base_path)
        if check_move:
            self.view.move_button.configure(state="enabled")

    def move_data(self, event) -> None:
        """
        Move the data from cleanup dir to the selected dirs depending
        on its data category.
        """
        total_moved, total_not_moved = 0, 0
        base_path = self.get_path_from_setup(name="Base-Path")
        for category,data in self.sorted_dict.items():
            if category != "unknown":
                target_path = self.get_path_from_setup(name=category)
                if target_path == "":
                    self.view.error_missing_target_path(category)
                    return
                else:
                    target_files = os.listdir(target_path)
                    for element in data:
                        if element not in target_files:
                            os.replace(os.path.join(base_path, element), os.path.join(target_path, element))
                            total_moved += 1
                        else:
                            total_not_moved += 1
        self.view.info_show_move_result(total_moved=total_moved, total_not_moved=total_not_moved)
        self.view.move_button.configure(state="disabled")
        self.analyze_data(event=None)

    def sort_data(self, data) -> None:
        """
        Sort the found data by data category ending and add it to 
        the corresponding known/unknown data list.
        """
        name, endings = data, data.split(".")[-1]
        for data_type in self.data_types:
            if endings in data_type.endings:
                self.sorted_dict[data_type.name].append(name)
                return
        self.sorted_dict["unknown"].append(name)
        
    def run(self) -> None:
        """
        Start the view mainloop.
        """
        self.view.mainloop()