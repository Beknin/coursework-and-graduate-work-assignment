import tkinter as tk
from tkinter import ttk
from api.client import APIClient
from gui.login_window import LoginWindow

class App:
    def __init__(self, title: str, user: dict, api_client: APIClient):
        self.user = user
        self.api = api_client
        self.window = tk.Toplevel()
        self.window.title(title)
        self.window.geometry("900x600")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self._create_widgets()

    def _create_widgets(self):
        pass

    def on_close(self):
        self.api.clear_token()
        self.window.destroy()
        LoginWindow()

    def show_error(self, message: str):
        from tkinter import messagebox
        messagebox.showerror("Ошибка", message)

    def show_info(self, message: str):
        from tkinter import messagebox
        messagebox.showinfo("Информация", message)