import ttkbootstrap as tb
from ttkbootstrap.tooltip import ToolTip


class SetupOptionPopup(tb.Toplevel):
    def __init__(self) -> None:
        super().__init__()
        self.title("Setup Path")
        self.resizable(False, False)
        self.init_ui()

    def init_ui(self) -> None:
        self.name_label = tb.Label(self, text="Name:")
        self.name_entry = tb.Entry(self, width=30)
        self.add_path_btn = tb.Button(self, text="Add Path", bootstyle="info-outline")
        self.file_format_label = tb.Label(self, text="File Formats:")
        self.file_format_entry = tb.Entry(self, width=30, )
        self.save_btn = tb.Button(self, text="save", bootstyle="success-outline")
        self.name_label.pack(padx=10, pady=(10, 5), anchor="w")
        self.name_entry.pack(padx=10, pady=5, anchor="w")
        self.file_format_label.pack(padx=10, pady=5, anchor="w")
        self.file_format_entry.pack(padx=10, pady=5, anchor="w")
        self.add_path_btn.pack(padx=10, pady=5, anchor="w")
        self.save_btn.pack(padx=10, pady=(5,10), anchor="w")
        ToolTip(self.file_format_label, text=f'Enter file format seperated by ",": doc, docx, pdf')

    def save_btn_on_click(self, callback) -> None:
        self.save_btn.bind("<Button-1>", callback)
