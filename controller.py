from view import View
from model import Model
from tkinter import filedialog as fd
from default_data.data_formats import *
from datatype import DataTypeCategory, DataType
import os
from data_option import DataOption

#for referencing
from widgets.select_opiton import SelectOption
from widgets.setup_option import SetupOptionPopup


class Controller():
    def __init__(self, view: View, model: Model) -> None:
        self.view = view
        self.model = model
        self.create_default_data_categories()
        self.create_default_widgtes()
        self.init_binds()

    def create_default_widgtes(self) -> None:
        """
        Create all default path widgets.
        """
        self.view.create_select_path_widget(root=self.view.base_path_frame, label="Base-Path", 
                                            directory=self.model.get_path("cleanup"), 
                                            callback=self.save_dir, 
                                            cancel=False)
        for data in self.data_type_categories:
            self.view.create_select_path_widget(root=self.view.target_path_frame, 
                                    label=data.name, directory=self.model.get_path(data.name), 
                                    callback= self.save_dir,
                                    cancel=True,
                                    tip=f"{data.endings}")
        
    def init_binds(self) -> None:
        """
        Bind the view's buttons to controllers methods.
        """
        self.view.add_btn_on_click(self.setup_new_data_option)
        self.view.check_btn_on_click(self.analyze_data)
        self.view.move_btn_on_click(self.move_data)
        
    def setup_new_data_option(self, event) -> None:
        new_path = self.view.create_new_path()
        new_path.save_btn_on_click(lambda event=event, new_path=new_path: self.save_data_option(event, new_path))

    def save_data_option(self, event, new_path:SetupOptionPopup) -> None:
        file_format_list = new_path.file_format_entry.get().split(",")
        file_format = {ending for ending in file_format_list}
        new_option = DataOption(name=new_path.name_entry.get(),
               path=None,
               file_format=file_format)
        print(new_option)

    def create_default_data_categories(self) -> None:
        """
        Create data type category instances with name and corresponding
        endings.
        """
        self.data_type_categories = [DataTypeCategory(name="documents", endings=DOCUMENTS),
                                     DataTypeCategory(name="pictures", endings=PICTURES),
                                     DataTypeCategory(name="videos", endings=VIDEOS),
                                     DataTypeCategory(name="music", endings=MUSIC),
                                     DataTypeCategory(name="executables", endings=EXECUTABLES)]

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
        if self.model.get_path("cleanup"):
            files = os.listdir(self.model.get_path("cleanup"))
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
                self.view.display_results(label=data_category.name, amount=len(data_category.list), path=self.model.get_path("cleanup"))#row=row,
                total_known += 1
            else:
                total_unknown += 1
        self.view.display_results(label="undefined data types", amount=total_unknown, path=self.model.get_path("cleanup"))
        if total_known == 0 and total_unknown == 0:
            self.view.display_results(label="elements", amount=0, path=self.model.get_path("cleanup"))#row=row,
        if total_known > 0:
            self.view.move_button.configure(state="enabled")

    def move_data(self, event) -> None:
        """
        Move the data from cleanup dir to the selected dirs depending
        on its data category.
        """
        for data_category in self.data_type_categories:
            for data in data_category.list:
                if self.model.get_path(data_category.name):
                    os.replace(os.path.join(self.model.get_path("cleanup"), data.name), os.path.join(self.model.get_path(data_category.name), data.name))
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
        ending = data.split(".")
        datatype = DataType(name=data, ending=ending[-1])
        print(datatype)
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