import ttkbootstrap as tb
from ttkbootstrap.dialogs.dialogs import Messagebox
from widgets.select_opiton import SelectOption
from widgets.setup_option import SetupOptionPopup
from widgets.result_widget import ResultWidget
from tkinter import filedialog


class View(tb.Window):
    def __init__(self) -> None:
        super().__init__(themename="darkly")
        self.title("FileOrganizer")
        self.resizable(False, False)
        self.base_path_frame = tb.Frame(self)
        self.base_path_frame.pack(padx=5, pady=5)

        tb.Separator(self).pack(fill="x")
        
        self.target_path_frame = tb.Frame(self)
        self.target_path_frame.pack(padx=5, pady=5)
        self.add_path_frame = tb.Frame(self)
        self.add_path_frame.pack(padx=5, pady=5, fill="x")
        self.add_btn = tb.Button(self.add_path_frame, bootstyle="light-outline",text="+")
        self.add_btn.pack(side="left", padx=10, pady=5)
        self.set_default = tb.Button(self.add_path_frame, bootstyle="light-outline",text="default")
        self.set_default.pack(side="right", padx=10, pady=(5,10))
        
        tb.Separator(self).pack(fill="x")
        
        self.bottom_frame = tb.Frame(self)
        self.bottom_frame.pack(padx=5, pady=5)
        self.check_btn = tb.Button(self.bottom_frame, bootstyle="success-outline", text="check")
        self.check_btn.pack(padx=5, pady=5, side="left")
        self.move_button = tb.Button(self.bottom_frame, text="move")
        self.move_button.pack(padx=5, pady=5, side="left")
        self.move_button.configure(state="disabled")

        tb.Separator(self).pack(fill="x")

        self.result_frame = tb.Frame(self)
        self.result_frame.pack(padx=5, pady=5, side="left")

    def default_btn_on_click(self, callback) -> None:
        self.set_default.bind("<Button-1>", callback)

    def check_btn_on_click(self, callback) -> None:
        self.check_btn.bind("<Button-1>", callback)

    def move_btn_on_click(self, callback) -> None:
        self.move_button.bind("<Button-1>", callback)

    def add_btn_on_click(self, callback) -> None:
        self.add_btn.bind("<Button-1>", callback)

    def edit_setup(self, setup) -> SetupOptionPopup:
        return SetupOptionPopup(setup)

    def create_new_setup(self) -> SetupOptionPopup:
        return SetupOptionPopup()

    def create_select_path_widget(self, root, edit_callback, delete_callback, label:str, directory:str="", cancel:bool=False, tip=None) -> None:
        SelectOption(root, edit_callback,delete_callback, label, directory, cancel, tip).pack(padx=5, pady=2)

    def clear_result_frame(self) -> None:
        if self.result_frame.winfo_children():
            for child in self.result_frame.winfo_children():
                child.destroy()

    def error_invalid_data_type_name(self, name, popup:SetupOptionPopup) -> None:
        message_box = Messagebox().show_error(title="Error", message=f"Invalid data type name {name}.")
        popup.lift()
        
    def info_enter_a_path(self, popup:SetupOptionPopup) -> None:
        message_box = Messagebox.show_info(title="Info", message="Please enter a valid path.")
        popup.lift()

    def display_results(self, label, amount, path) -> None:
        ResultWidget(root=self.result_frame, label=label, amount=amount, path=path).pack(padx=5, pady=2)

    def destroy_child_widgets(self, parent_frame:tb.Frame) -> None:
        """
        Destroy all child widgets inside of a frame.
        """
        for child in parent_frame.winfo_children():
            child.destroy()

    @staticmethod
    def set_dir(name=None) -> str:
        if name:
            return filedialog.askdirectory(title=f"Set {name} directory")
        return filedialog.askdirectory()