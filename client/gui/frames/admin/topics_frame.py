from tkinter import ttk, messagebox
from gui.widgets.table_view import TableView
from api.topics_api import TopicsAPI
from api.users_api import UsersAPI
from gui.dialogs.topic_dialog import TopicDialog


class TopicsFrame(ttk.Frame):
    def __init__(self, parent, api_client):
        super().__init__(parent)
        self.api = TopicsAPI(api_client)
        self.users_api = UsersAPI(api_client)

        columns = ["id", "title", "level", "teacher_name", "status"]
        column_names = {
            "id": "ID",
            "title": "Название",
            "level": "Тип",
            "teacher_name": "Преподаватель",
            "status": "Статус",
        }
        self.table = TableView(self, columns, column_names)
        self.table.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Добавить", command=self._add).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Редактировать", command=self._edit).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Удалить", command=self._delete).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Обновить", command=self._load).pack(side="right", padx=2)

        self._load()

    def _load(self):
        try:
            topics = self.api.get_topics()
            teachers = self.users_api.get_all_users()
            teacher_map = {t['id']: t['full_name'] for t in teachers if t['role'] == 'teacher'}

            for topic in topics:
                topic['teacher_name'] = teacher_map.get(topic.get('teacher_id'), 'Неизвестный')
                topic['level'] = "Курсовая" if topic.get('level') == 'coursework' else "Диплом"

            self.table.set_data(topics)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить темы:\n{e}")

    def _add(self):
        teachers = [t for t in self.users_api.get_all_users() if t['role'] == 'teacher']
        if not teachers:
            messagebox.showwarning("Предупреждение", "Сначала добавьте преподавателей")
            return

        dialog = TopicDialog(self, teachers=teachers)
        if dialog.result:
            try:
                self.api.create_topic(dialog.result)
                self._load()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def _edit(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите тему для редактирования")
            return

        teachers = [t for t in self.users_api.get_all_users() if t['role'] == 'teacher']
        dialog = TopicDialog(self, topic=selected, teachers=teachers)
        if dialog.result:
            try:
                self.api.update_topic(selected['id'], dialog.result)
                self._load()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def _delete(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите тему для удаления")
            return
        if messagebox.askyesno("Подтверждение", f"Удалить тему «{selected['title']}»?"):
            try:
                self.api.delete_topic(selected['id'])
                self._load()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))