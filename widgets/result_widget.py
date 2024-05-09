import ttkbootstrap as tb


class ResultWidget(tb.Frame):
    def __init__(self, root, label, amount, path) -> None:
        super().__init__(root)
        self.text = f"Found {amount} {label} in {path}"
        self.setup_ui()

    def setup_ui(self) -> None:
        self.label = tb.Label(self, text=self.text)
        self.label.pack(padx=5, pady=5)