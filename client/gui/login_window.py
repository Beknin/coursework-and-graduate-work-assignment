import tkinter as tk
from tkinter import ttk
from api.client import APIClient
from api.auth_api import MockAuthAPI

class LoginWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Вход в систему")
        self.geometry("400x300")
        self.resizable(False, False)

        self.api_client = APIClient()
        self.auth_api = MockAuthAPI()

        self._create_widgets()

    def _create_widgets(self):
        # Заголовок
        ttk.Label(self, text="🎓 Распределение работ",
                  font=("Arial", 14, "bold")).pack(pady=20)

        # Фрейм с полями
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        ttk.Label(frame, text="Логин:").grid(row=0, column=0, sticky="e", pady=5)
        self.login_entry = ttk.Entry(frame, width=25)
        self.login_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Пароль:").grid(row=1, column=0, sticky="e", pady=5)
        self.password_entry = ttk.Entry(frame, width=25, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        # Выбор роли
        ttk.Label(frame, text="Роль:").grid(row=2, column=0, sticky="e", pady=5)
        self.role_var = tk.StringVar(value="student")
        role_frame = ttk.Frame(frame)
        role_frame.grid(row=2, column=1, pady=5)
        ttk.Radiobutton(role_frame, text="Администратор",
                        variable=self.role_var, value="admin").pack(side="left")
        ttk.Radiobutton(role_frame, text="Преподаватель",
                        variable=self.role_var, value="teacher").pack(side="left")
        ttk.Radiobutton(role_frame, text="Студент",
                        variable=self.role_var, value="student").pack(side="left")

        # Кнопки
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Войти", command=self._login).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Выход", command=self.destroy).pack(side="left", padx=5)

        # Статус сервера
        self.status_label = ttk.Label(self, text="Проверка подключения...")
        self.status_label.pack(side="bottom", pady=10)

        # Enter = Войти
        self.bind("<Return>", lambda e: self._login())

    def _login(self):
        login = self.login_entry.get().strip()
        password = self.password_entry.get()
        role = self.role_var.get()

        if not login or not password:
            self._show_error("Заполните все поля")
            return

        try:
            result = self.auth_api.login(login, password, role)
            self.api_client.set_token(result["token"])
            self._open_role_window(result["user"])
            self.destroy()
        except Exception as e:
            self._show_error(str(e))

    def _open_role_window(self, user: dict):
        role = user["role"]
        if role == "admin":
            from gui.admin_window import AdminWindow
            AdminWindow(user, self.api_client)
        elif role == "teacher":
            from gui.teacher_window import TeacherWindow
            TeacherWindow(user, self.api_client)
        elif role == "student":
            from gui.student_window import StudentWindow
            StudentWindow(user, self.api_client)

    def _show_error(self, message):
        from tkinter import messagebox
        messagebox.showerror("Ошибка", message)