from __future__ import annotations
from typing import TYPE_CHECKING
import os
from model import DataType
from crud.data_type import (
    db_get_all_data_types,
    db_delete_all_data_types,
    db_delete_data_type_by_name,
    db_get_data_type_by_name,
    db_insert_data_type,
    db_update_data_type,
)
from default_data.data_formats import DEFAULT_DATA_FORMATS

if TYPE_CHECKING:
    from widgets.setup_option import SetupOptionPopup
    from view import View


class Controller:
    def __init__(self, view: View) -> None:
        self.view = view
        self.check_load_default_data()
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
        self.reset_data_type_db()
        self.reset_all_widgets()

    def reset_all_widgets(self) -> None:
        self.check_load_default_data()
        self.view.destroy_child_widgets(self.view.target_path_frame)
        self.view.destroy_child_widgets(self.view.base_path_frame)
        self.view.destroy_child_widgets(self.view.result_frame)
        self.update_all_setup_widgets()

    def reset_data_type_db(self) -> None:
        """
        Resets the path.json file to default (empty paths).
        """
        db_delete_all_data_types()
        db_insert_data_type(DataType(name="Base-Path"))
        for key, val in DEFAULT_DATA_FORMATS.items():
            db_insert_data_type(DataType(name=key, endings=list(val)))

    def check_load_default_data(self) -> None:
        """
        Get all elements from path.json and data_type.json.
        Creates DataType and DataSetup instance.
        """
        data_types_json = db_get_all_data_types()
        if not data_types_json:
            for name, endings in DEFAULT_DATA_FORMATS.items():
                data_type = DataType(name=name, endings=endings)
                db_insert_data_type(data_type=data_type)

    def update_all_setup_widgets(self) -> None:
        """
        Create all default path widgets.
        """
        self.create_base_widget()
        data_types = db_get_all_data_types()
        for data in data_types:
            if data.name.lower() != "base-path":
                self.create_setup_widget(data)

    def create_setup_widget(self, data_type: DataType) -> None:
        """
        Helper function updating the setup widgets of the view.
        """
        self.view.create_select_path_widget(
            root=self.view.target_path_frame,
            label=data_type.name,
            directory=data_type.path,
            edit_callback=self.edit_data_type,
            delete_callback=lambda event, name=data_type.name: db_delete_data_type_by_name(
                name
            ),
            cancel=True,
            tip=f"{data_type.endings}",
        )

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
        self.view.create_select_path_widget(
            root=self.view.base_path_frame,
            label="Base-Path",
            directory=(
                db_get_data_type_by_name("Base-Path").path
                if db_get_data_type_by_name("Base-Path")
                else ""
            ),
            edit_callback=self.edit_base_path,
            delete_callback=None,
            cancel=False,
        )

    def edit_base_path(self, event, name: str) -> None:
        """
        Edits the base path by validating the chosen path, adding
        it to the DBs and temp lists and updating the view.
        """
        print("Editing base path")
        path = self.view.set_dir()
        if name.lower() != "base-path" or path == "":
            return "break"
        data_type = db_get_data_type_by_name(name=name)
        if not data_type:
            data_type = DataType(name=name)
            db_insert_data_type(data_type)
        data_type.path = path
        db_update_data_type(name=data_type.name, data_type=data_type)
        self.update_base_view()
        return "break"

    def edit_data_type(self, event, name: str) -> None:
        """
        Takes the name of a setup and opens a prefilled
        edit setup view.
        """
        data_type = db_get_data_type_by_name(name)
        if not data_type:
            print("No data type found for editing.")
            return "break"
        edit_setup = self.view.edit_setup(data_type)
        edit_setup.save_btn_on_click(
            lambda event=event, edit_setup=edit_setup, data_type=data_type: self.save_setup_data_edit(
                event, edit_setup, data_type
            )
        )

    def save_setup_data_edit(
        self, event, edit_setup: SetupOptionPopup, data_type: DataType
    ) -> None:
        """
        Save edited setup. Only validate the path, since the name
        cannot be changed in the frontend. Remove the old elements from
        temp lists and DBs and add the new once.
        """
        new_endings = edit_setup.file_format_entry.get()
        endings = new_endings.split(",")
        path = edit_setup.dir
        db_update_data_type(
            name=data_type.name,
            data_type=DataType(name=data_type.name, endings=endings, path=path),
        )
        if path is None or path == "":
            self.view.info_enter_a_path(edit_setup)
            raise ValueError("Path cannot be empty.")
        self.reset_all_widgets()
        edit_setup.destroy()

    def create_new_setup(self, event) -> None:
        """
        Opens a new setup popup and binds the save method
        to it.
        """
        new_setup = self.view.create_new_setup()
        new_setup.save_btn_on_click(
            lambda event=event, new_setup=new_setup: self.save_setup_data(
                event, new_setup
            )
        )

    def save_setup_data(self, event, new_option: SetupOptionPopup) -> None:
        """
        Validates the newly created data, adds it in to the temp data/setup lists
        and adds it to the DBs.
        """
        data_type = self.validate_new_data(new_option)
        if data_type:
            self.create_setup_widget(data_type=data_type)
            new_option.destroy()

    def validate_new_data(self, new_option: SetupOptionPopup) -> DataType | None:
        """
        Validates data of te SetupOptionPopup and returns it
        if validation is successfull.
        """
        file_formats = {
            ending for ending in new_option.file_format_entry.get().split(",")
        }
        name = new_option.name_entry.get()
        if name.strip() == "":
            self.view.error_invalid_data_type_name("''", new_option)
            return None
        if new_option.dir is None or new_option.dir.strip() == "":
            self.view.info_enter_a_path(new_option)
            return None
        try:
            new_data_type = db_insert_data_type(
                data_type=DataType(name=name, endings=file_formats)
            )
        except ValueError:
            self.view.error_invalid_data_type_name(f"'{name.lower()}'", new_option)
            return None
        return new_data_type

    def analyze_data(self, event) -> None:
        """
        Analize the data in the cleanup path.
        """
        self.sorted_dict = self.create_sorting_dictionary()
        path = db_get_data_type_by_name("Base-Path").path
        if path != "":
            files = os.listdir(path)
            for element in files:
                self.sort_data(data=element)
        else:
            self.view.info_select_base_dir()
        self.display_findings()

    def create_sorting_dictionary(self) -> dict:
        all_data_types = db_get_all_data_types()
        if not all_data_types:
            raise ValueError("No data types found in the database.")
        sort_dict = {"unknown": []}
        for data_type in all_data_types:
            sort_dict[data_type.name] = []
        return sort_dict

    def display_findings(self) -> None:
        """
        Show all findings from the cleanup path.
        """
        check_move = False
        base_path = (
            db_get_data_type_by_name("Base-Path").path
            if db_get_data_type_by_name("Base-Path")
            else ""
        )
        self.view.destroy_child_widgets(self.view.result_frame)
        for data in db_get_all_data_types():
            if self.sorted_dict[data.name]:
                self.view.display_results(
                    label=data.name,
                    amount=len(self.sorted_dict[data.name]),
                    path=base_path,
                )
                check_move = True
        if self.sorted_dict["unknown"]:
            self.view.display_results(
                label="undefined data types",
                amount=len(self.sorted_dict["unknown"]),
                path=base_path,
            )
        if check_move:
            self.view.move_button.configure(state="enabled")

    def move_data(self, event) -> None:
        """
        Move the data from cleanup dir to the selected dirs depending
        on its data category.
        """
        total_moved, total_not_moved = 0, 0
        base_path = db_get_data_type_by_name("Base-Path").path
        if not base_path:
            self.view.info_select_base_dir()
            return
        for category, data in self.sorted_dict.items():
            if category != "unknown":
                target_path = db_get_data_type_by_name(category).path
                if not target_path:
                    self.view.error_missing_target_path(category)
                    return
                else:
                    target_files = os.listdir(target_path)
                    for element in data:
                        if element not in target_files:
                            os.replace(
                                os.path.join(base_path, element),
                                os.path.join(target_path, element),
                            )
                            total_moved += 1
                        else:
                            total_not_moved += 1
        self.view.info_show_move_result(
            total_moved=total_moved, total_not_moved=total_not_moved
        )
        self.view.move_button.configure(state="disabled")
        self.analyze_data(event=None)

    def sort_data(self, data) -> None:
        """
        Sort the found data by data category ending and add it to
        the corresponding known/unknown data list.
        """
        name, endings = data, data.split(".")[-1]
        data_types = db_get_all_data_types()
        for data_type in data_types:
            if endings in data_type.endings:
                self.sorted_dict[data_type.name].append(name)
                return
        self.sorted_dict["unknown"].append(name)

    def run(self) -> None:
        """
        Start the view mainloop.
        """
        self.view.mainloop()
