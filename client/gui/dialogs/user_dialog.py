import tkinter as tk
from tkinter import ttk

class UserDialog(tk.Toplevel):
    def __init__(self, parent, user: dict = None):
        super().__init__(parent)
        self.result = None
        self.title("Редактировать" if user else "Добавить пользователя")
        self.geometry("350x300")
        self.resizable(False, False)

        # Поля
        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="ФИО:").grid(row=0, column=0, sticky="e", pady=5)
        self.full_name = ttk.Entry(frame, width=30)
        self.full_name.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Логин:").grid(row=1, column=0, sticky="e", pady=5)
        self.login = ttk.Entry(frame, width=30)
        self.login.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Пароль:").grid(row=2, column=0, sticky="e", pady=5)
        self.password = ttk.Entry(frame, width=30, show="*")
        self.password.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Роль:").grid(row=3, column=0, sticky="e", pady=5)
        self.role = ttk.Combobox(frame, values=["admin", "teacher", "student"], width=27)
        self.role.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text="Группа/Кафедра:").grid(row=4, column=0, sticky="e", pady=5)
        self.group_dep = ttk.Entry(frame, width=30)
        self.group_dep.grid(row=4, column=1, pady=5)

        # Если редактирование — заполняем поля
        if user:
            self.full_name.insert(0, user.get("full_name", ""))
            self.login.insert(0, user.get("login", ""))
            self.role.set(user.get("role", ""))
            self.group_dep.insert(0, user.get("group") or user.get("department", ""))

        # Кнопки
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Сохранить", command=self._on_save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.destroy).pack(side="left", padx=5)

        self.grab_set()
        self.wait_window()

    def _on_save(self):
        self.result = {
            "full_name": self.full_name.get().strip(),
            "login": self.login.get().strip(),
            "password": self.password.get(),
            "role": self.role.get(),
            "group": self.group_dep.get().strip() if self.role.get() == "student" else None,
            "department": self.group_dep.get().strip() if self.role.get() == "teacher" else None,
        }
        self.destroy()