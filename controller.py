from view import View
from model import Model
from tkinter import filedialog as fd
from datatype import DataTypeCategory, DataType
import os


class Controller():
    def __init__(self, view: View, model: Model) -> None:
        self.view = view
        self.model = model
        self.init_dirs()
        self.init_binds_on_view()
        self.init_check_bind()
        self.create_data_categories()

    def init_binds_on_view(self) -> None:
        """
        Initiate all button bindings in the view.
        """
        self.view.cleanup_btn_on_click(lambda event, name="cleanup", view_element=self.view.cleanup: self.save_dir(event, name, view_element))
        self.view.documents_btn_on_click(lambda event, name="documents", view_element=self.view.documents: self.save_dir(event, name, view_element))
        self.view.pictures_btn_on_click(lambda event, name="pictures", view_element=self.view.pictures: self.save_dir(event, name, view_element))
        self.view.videos_btn_on_click(lambda event, name="videos", view_element=self.view.videos: self.save_dir(event, name, view_element))
        self.view.music_btn_on_click(lambda event, name="music", view_element=self.view.music: self.save_dir(event, name, view_element))
        self.view.execute_btn_on_click(lambda event, name="execute", view_element=self.view.execute: self.save_dir(event, name, view_element))
        
    def init_check_bind(self) -> None:
        """
        Bind the views check button.
        """
        self.view.check_btn_on_click(self.analyze_data)

    def init_move_bind(self) -> None:
        """
        Bind the views move button.
        """
        self.view.move_btn_on_click(self.move_data)
    
    def init_dirs(self) -> None:
        """
        Set the directories in the view to the once that have been saved
        in the userdata json file.
        """
        self.view.cleanup.dir.configure(text=self.model.get_path("cleanup"))
        self.view.documents.dir.configure(text=self.model.get_path("documents"))
        self.view.pictures.dir.configure(text=self.model.get_path("pictures"))
        self.view.videos.dir.configure(text=self.model.get_path("videos"))
        self.view.music.dir.configure(text=self.model.get_path("music"))
        self.view.execute.dir.configure(text=self.model.get_path("execute"))

    def create_data_categories(self) -> None:
        """
        Create data type category instances with name and corresponding
        endings.
        """
        self.documents = DataTypeCategory(name="documents", endings=set(["doc", "docx", "pdf", "rtf", "txt", "odt", "md", "html", "htm", "xls", "xlsx"]))
        self.pictures = DataTypeCategory(name="pictures", endings=set(["jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "psd", "svg"]))
        self.videos = DataTypeCategory(name="videos", endings=set(["mp4", "avi", "mov", "wmv", "flv", "mkv", "webm"]))
        self.music = DataTypeCategory(name="music", endings=set(["mp3", "wav", "aac", "flac", "ogg", "wma", "aiff", "aif"]))
        self.execute = DataTypeCategory(name="executables", endings=set(["exe", "bat", "cmd", "com", "msi", "jar", "js"]))
        self.other = DataTypeCategory(name="other", endings=None)

    def save_dir(self, event, name, view_element) -> None:
        """
        Safe a path for the selected categgory to the user data json.
        """
        path = self.view.set_dir(name)
        if path:
            view_element.dir.configure(text=path)
            self.model.save_path(name=name, path=path)

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
        row = 1
        for data_category in [self.pictures, self.documents, self.videos, self.music, self.execute]:
            if data_category.list:
                self.view.display_results(label=data_category.name, amount=len(data_category.list), row=row, path=self.model.get_path("cleanup"))
                row+=1
        if row > 1:
            self.view.create_move_button(row=row)
            self.init_move_bind()
        else:
            #if no element has been found
            self.view.display_results(label="elements", amount=0, row=row, path=self.model.get_path("cleanup"))

    def move_data(self, event) -> None:
        """
        Move the data from cleanup dir to the selected dirs depending
        on its data category.
        """
        for data in self.documents.list:
            if self.model.get_path("documents"):
                os.replace(os.path.join(self.model.get_path("cleanup"), data.name), os.path.join(self.model.get_path("documents"), data.name))
            else:
                self.save_dir(event, name="documents", view_element=self.view.documents)
        for data in self.pictures.list:
            if self.model.get_path("pictures"):
                os.replace(os.path.join(self.model.get_path("cleanup"), data.name), os.path.join(self.model.get_path("pictures"), data.name))
            else:
                self.save_dir(event, name="pictures", view_element=self.view.pictures)
        for data in self.videos.list:
            if self.model.get_path("videos"):
                os.replace(os.path.join(self.model.get_path("cleanup"), data.name), os.path.join(self.model.get_path("videos"), data.name))
            else:
                self.save_dir(event, name="videos", view_element=self.view.videos)
        for data in self.music.list:
            if self.model.get_path("music"):
                os.replace(os.path.join(self.model.get_path("cleanup"), data.name), os.path.join(self.model.get_path("music"), data.name))
            else:
                self.save_dir(event, name="music", view_element=self.view.music)
        for data in self.execute.list:
            if self.model.get_path("execute"):
                os.replace(os.path.join(self.model.get_path("cleanup"), data.name), os.path.join(self.model.get_path("execute"), data.name))
            else:
                self.save_dir(event, name="execute", view_element=self.view.execute)
        self.update_bottom_view(event)

    def update_bottom_view(self, event) -> None:
        """
        Update the view displaying the data check results.
        """
        for widget in self.view.bottom_frame.winfo_children():
            widget.destroy()
            self.analyze_data(event)
            self.view.create_check_button()
            self.init_check_bind()

    def sort_data(self, data) -> None:
        """
        Sort the found data by data category ending and add it to 
        the corresponding data category list.
        """
        ending = data.split(".")
        datatype = DataType(name=data, ending=ending[-1])
        for data_category in [self.pictures, self.documents, self.videos, self.music, self.execute]:
            if datatype.ending in data_category.endings:
                data_category.list.append(datatype)
            else: self.other.list.append(datatype)

    def clear_data(self) -> None:
        """
        Clear all lists of the data category instances.
        """
        for data in [self.pictures, self.documents, self.videos, self.music, self.execute, self.other]:
            data.list = []
        
    def run(self) -> None:
        """
        Start the view mainloop.
        """
        self.view.mainloop()