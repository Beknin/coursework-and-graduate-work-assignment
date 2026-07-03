from tkinter import ttk
from gui.app import App
from gui.widgets.status_bar import StatusBar
from gui.frames.admin.users_frame import UsersFrame
from gui.frames.admin.topics_frame import TopicsFrame


class AdminWindow(App):
    def __init__(self, user: dict, api_client):
        super().__init__(f"Панель администратора — {user.get('full_name', 'Admin')}", user, api_client)

    def _create_widgets(self):
        header = ttk.Frame(self.window)
        header.pack(fill="x", padx=10, pady=5)
        ttk.Label(
            header,
            text=f"👤 {self.user.get('full_name', 'Admin')} (admin)",
            font=("Arial", 11)
        ).pack(side="left")
        ttk.Button(header, text="Выйти", command=self.on_close).pack(side="right")

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.users_frame = UsersFrame(notebook, self.api)
        notebook.add(self.users_frame, text="Пользователи")

        self.topics_frame = TopicsFrame(notebook, self.api)
        notebook.add(self.topics_frame, text="Темы")

        for tab_name in ["Назначения", "Отчёты"]:
            frame = ttk.Frame(notebook)
            ttk.Label(frame, text=f"Вкладка: {tab_name}").pack(expand=True)
            notebook.add(frame, text=tab_name)

        self.status_bar = StatusBar(self.window)
        self.status_bar.set_status("Готово | Администратор")