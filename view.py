import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organizer")
        self.resizable(False, False)
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(padx=10, pady=10)
        self.seperator_1 = ttk.Separator(self)
        self.seperator_1.pack(fill="x")
        self.mid_frame = ttk.Frame(self)
        self.mid_frame.pack(padx=10, pady=5)
        self.seperator_2 = ttk.Separator(self)
        self.seperator_2.pack(fill="x")
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(padx=10, pady=5)

        self.cleanup = SelectPathWidget(root=self.top_frame, label="Cleanup", directory="")
        self.cleanup.grid_all(row=0)
        self.documents = SelectPathWidget(root=self.mid_frame, label="Documents", directory="")
        self.documents.grid_all(row=2)
        self.pictures = SelectPathWidget(root=self.mid_frame, label="Pictures", directory="")
        self.pictures.grid_all(row=3)
        self.videos = SelectPathWidget(root=self.mid_frame, label="Videos", directory="")
        self.videos.grid_all(row=4)
        self.music = SelectPathWidget(root=self.mid_frame, label="Music", directory="")
        self.music.grid_all(row=5)
        self.execute = SelectPathWidget(root=self.mid_frame, label="Executable", directory="")
        self.execute.grid_all(row=6)
        self.create_check_button()

    def cleanup_btn_on_click(self, callback):
         self.cleanup.button.bind("<Button-1>", callback)

    def documents_btn_on_click(self, callback):
         self.documents.button.bind("<Button-1>", callback) 

    def pictures_btn_on_click(self, callback):
         self.pictures.button.bind("<Button-1>", callback)

    def videos_btn_on_click(self, callback):
         self.videos.button.bind("<Button-1>", callback)

    def music_btn_on_click(self, callback):
         self.music.button.bind("<Button-1>", callback)

    def execute_btn_on_click(self, callback):
        self.execute.button.bind("<Button-1>", callback)

    def move_btn_on_click(self, callback):
        self.move_button.bind("<Button-1>", callback)

    def check_btn_on_click(self, callback):
         self.check_btn.bind("<Button-1>", callback)
      
    @staticmethod
    def set_dir(name=None):
        if name:
            return filedialog.askdirectory(title=f"Set {name} directory")
        return filedialog.askdirectory()
    
    def display_results(self, label, amount, row, path):
        widget = DisplayOccurancesWidget(root=self.bottom_frame, label=label, amount=amount, path=path)
        widget.grid_all(row=row)

    def create_check_button(self):
        self.check_btn = ttk.Button(self.bottom_frame, text="check")
        self.check_btn.grid(row=0, column=0, padx=5, pady=5)

    def create_move_button(self, row):
        self.move_button = ttk.Button(self.bottom_frame, text="move")
        self.move_button.grid(row=row, column=0, padx=5, pady=5)
    

class SelectPathWidget():
    def __init__(self, root, label, directory):
        self.label = ttk.Label(root, text=label, width=15)
        self.dir = ttk.Label(root, text=directory)
        self.button = ttk.Button(root, text="edit")

    def grid_all(self, row):
        self.label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        self.dir.grid(row=row, column=1, padx=5, pady=5, sticky="w")
        self.button.grid(row=row, column=2, padx=5, pady=5, sticky="w")

class DisplayOccurancesWidget():
    def __init__(self, root, label, amount, path):
        text = f"Found {amount} {label} in {path}"
        self.label = ttk.Label(root, text=text)

    def grid_all(self, row):
        self.label.grid(row=row, column=0, padx=5, pady=5, sticky="w")