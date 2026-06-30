import tkinter as tk
from tkinter import ttk

class StatusBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side="bottom", fill="x")

        self.label = ttk.Label(self, text="Готово", relief="sunken", anchor="w")
        self.label.pack(fill="x")

    def set_status(self, text: str):
        self.label.config(text=text)