from __future__ import annotations
from typing import TYPE_CHECKING
import ttkbootstrap as tb
from ttkbootstrap.tooltip import ToolTip
from tkinter import filedialog

if TYPE_CHECKING:
    from model import DataType, DataTypePathConfig


class SetupOptionPopup(tb.Toplevel):
    def __init__(self, data_type: DataType = None) -> None:
        super().__init__()
        self.title("Setup Path")
        self.resizable(False, False)
        self.dir = None
        self.init_ui()
        if data_type:
            self.prefill_setup(data_type)

    def init_ui(self) -> None:
        self.name_label = tb.Label(self, text="Name:")
        self.name_entry = tb.Entry(self, width=30)
        self.add_path_btn = tb.Button(self, text="Add Path", bootstyle="info-outline")
        self.file_format_label = tb.Label(self, text="File Formats:")
        self.file_format_entry = tb.Entry(
            self,
            width=30,
        )
        self.path_label = tb.Label(self, text="")
        self.save_btn = tb.Button(self, text="save", bootstyle="success-outline")
        self.name_label.pack(padx=10, pady=(10, 5), anchor="w")
        self.name_entry.pack(padx=10, pady=5, anchor="w")
        self.file_format_label.pack(padx=10, pady=5, anchor="w")
        ToolTip(
            self.file_format_label,
            text=f'Enter file format seperated by ",": doc, docx, pdf',
        )
        self.file_format_entry.pack(padx=10, pady=5, anchor="w")
        self.add_path_btn.pack(padx=10, pady=5, anchor="w")
        self.path_label.pack(padx=10, pady=5, anchor="w")
        self.save_btn.pack(padx=10, pady=(5, 10), anchor="w")
        self.add_path_btn_on_click()

    def save_btn_on_click(self, callback) -> None:
        self.save_btn.bind("<Button-1>", callback)

    def add_path_btn_on_click(self) -> None:
        self.add_path_btn.bind("<Button-1>", self.get_dir)

    def get_dir(self, event) -> None:
        self.dir = filedialog.askdirectory()
        self.path_label.configure(text=self.dir)
        self.lift()
        return "break"

    def prefill_setup(self, data_type: DataType) -> None:
        self.name_entry.insert(0, data_type.name)
        self.name_entry.configure(state="readonly")
        for i, ending in enumerate(data_type.endings):
            if i == 0:
                self.file_format_entry.insert(0, f"{ending}")
            else:
                self.file_format_entry.insert(0, f"{ending},")
        # self.file_format_entry.insert(0, str(setup.data_type.endings)[1:-1])
        self.dir = data_type.path
        self.path_label.configure(text=self.dir)
