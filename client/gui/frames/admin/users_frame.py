from tkinter import ttk, messagebox
from gui.widgets.table_view import TableView
from client.api.users_api import UsersAPI
from client.gui.dialogs.user_dialog import UserDialog


class UsersFrame(ttk.Frame):
    def __init__(self, parent, api_client):
        super().__init__(parent)
        self.api = UsersAPI(api_client)

        columns = ["id", "full_name", "login", "role"]
        column_names = {
            "id": "ID",
            "full_name": "ФИО",
            "login": "Логин",
            "role": "Роль",
        }
        self.table = TableView(self, columns, column_names)
        self.table.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Добавить", command=self._add_user).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Редактировать", command=self._edit_user).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Удалить", command=self._delete_user).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Обновить", command=self._load_data).pack(side="right", padx=2)

        self._load_data()

    def _load_data(self):
        try:
            users = self.api.get_all_users()
            self.table.set_data(users)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить пользователей:\n{e}")

    def _add_user(self):
        dialog = UserDialog(self)
        if dialog.result:
            try:
                self.api.create_user(dialog.result)
                self._load_data()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def _edit_user(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя для редактирования")
            return
        dialog = UserDialog(self, selected)
        if dialog.result:
            try:
                self.api.update_user(selected["id"], dialog.result)
                self._load_data()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def _delete_user(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя для удаления")
            return
        if messagebox.askyesno("Подтверждение",
                               f"Удалить пользователя {selected['full_name']}?"):
            try:
                self.api.delete_user(selected["id"])
                self._load_data()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))