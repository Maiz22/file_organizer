import ttkbootstrap as tb
from ttkbootstrap.tooltip import ToolTip


class SelectOption(tb.Frame):
    def __init__(self, root, edit_callback, delete_callback, label:str, directory:str="", cancel=True, tip=None) -> None:
        super().__init__(root)
        self.label = label
        self.directory = directory
        self.edit_callback = lambda event, name=self.label: edit_callback(event, name) #, view_element , view_element=self
        self.delete_callback = lambda event, name=self.label: delete_callback(event,name)
        self.tip = tip
        self.init_ui()
        if cancel:
            self.add_active_cancel_btn()
        else:
            self.add_inactive_cancel_btn()

    def init_ui(self) -> None:
        self.label = tb.Label(self, text=self.label, width=20)
        self.dir = tb.Label(self, text=self.directory, width=40)
        self.edit_button = tb.Button(self, bootstyle="info-outline", text="edit")
        self.label.pack(padx=5, pady=2, side="left")
        self.dir.pack(padx=5, pady=2, side="left")
        self.edit_button.pack(padx=5, pady=2, side="left")
        self.edit_button.bind("<Button-1>", self.edit_callback)
        if self.tip is not None:
            ToolTip(self.label, text=self.tip)
    
    def add_active_cancel_btn(self) -> None:
        self.cancel_button = tb.Button(self, bootstyle="danger-outline", text="x", command=self.destroy)
        self.cancel_button.pack(padx=5, pady=2, side="left")
        self.cancel_button.bind("<Button-1>", self.delete_callback)

    def add_inactive_cancel_btn(self) -> None:
        self.cancel_button = tb.Button(self, bootstyle="disabled-outline", text="x",state="disabled")
        self.cancel_button.pack(padx=5, pady=2, side="left")