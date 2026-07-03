import tkinter as tk
from tkinter import ttk, messagebox
from gui.app import App
from gui.widgets.table_view import TableView
from gui.widgets.status_bar import StatusBar
from gui.dialogs.topic_dialog import TopicDialog


class TeacherWindow(App):
    def __init__(self, user, api_client):
        super().__init__(f"Преподаватель: {user.get('full_name', '')}", user, api_client)

    def _create_widgets(self):
        header = ttk.Frame(self.window)
        header.pack(fill="x", padx=10, pady=5)
        ttk.Label(
            header,
            text=f"👤 {self.user.get('full_name', '')} (преподаватель)",
            font=("Arial", 11)
        ).pack(side="left")
        ttk.Button(header, text="Выйти", command=self.on_close).pack(side="right")

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.my_topics_frame = MyTopicsFrame(notebook, self.api, self.user["id"])
        notebook.add(self.my_topics_frame, text="Мои темы")

        self.my_students_frame = MyStudentsFrame(notebook, self.api, self.user["id"])
        notebook.add(self.my_students_frame, text="Мои студенты")

        self.requests_frame = RequestsFrame(notebook, self.api, self.user["id"])
        notebook.add(self.requests_frame, text="Заявки")

        self.status_bar = StatusBar(self.window)
        self.status_bar.set_status(
            f"Преподаватель | {self.user.get('department', 'Кафедра не указана')}"
        )


class MyTopicsFrame(ttk.Frame):
    def __init__(self, parent, api_client, teacher_id):
        super().__init__(parent)
        self.api = api_client
        self.teacher_id = teacher_id

        columns = ["id", "title", "level", "status"]
        column_names = {
            "id": "ID",
            "title": "Название",
            "level": "Тип",
            "status": "Статус",
        }
        self.table = TableView(self, columns, column_names)
        self.table.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="➕ Добавить тему", command=self._add_topic).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="✏️ Редактировать", command=self._edit_topic).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="🗑 Удалить", command=self._delete_topic).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="🔄 Обновить", command=self._load).pack(side="right", padx=2)

        self._load()

    def _load(self):
        try:
            all_topics = self.api._request("GET", "/api/topics/")
            my_topics = [t for t in all_topics if t.get("teacher_id") == self.teacher_id]

            for t in my_topics:
                t["level"] = "Курсовая" if t.get("level") == "coursework" else "Диплом"
                status = t.get("status", "free")
                status_map = {
                    "free": "Свободна",
                    "assigned": "Занята",
                    "reserved": "Зарезервирована",
                    "taken": "Занята",
                }
                t["status"] = status_map.get(status, status)

            self.table.set_data(my_topics)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить темы:\n{e}")

    def _add_topic(self):
        dialog = TopicDialog(self)
        if dialog.result:
            dialog.result["teacher_id"] = self.teacher_id
            try:
                self.api._request("POST", "/api/topics/", json=dialog.result)
                messagebox.showinfo("Успех", "Тема добавлена!")
                self._load()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def _edit_topic(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите тему для редактирования")
            return

        dialog = TopicDialog(self, topic=selected)
        if dialog.result:
            dialog.result["teacher_id"] = self.teacher_id
            try:
                self.api._request("PUT", f"/api/topics/{selected['id']}", json=dialog.result)
                messagebox.showinfo("Успех", "Тема обновлена!")
                self._load()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def _delete_topic(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите тему для удаления")
            return

        if messagebox.askyesno("Подтверждение", f"Удалить тему «{selected['title']}»?"):
            try:
                self.api._request("DELETE", f"/api/topics/{selected['id']}")
                messagebox.showinfo("Успех", "Тема удалена!")
                self._load()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))


class MyStudentsFrame(ttk.Frame):
    def __init__(self, parent, api_client, teacher_id):
        super().__init__(parent)
        self.api = api_client
        self.teacher_id = teacher_id

        columns = ["student_name", "group_name", "topic_title", "status"]
        column_names = {
            "student_name": "Студент",
            "group_name": "Группа",
            "topic_title": "Тема",
            "status": "Статус",
        }
        self.table = TableView(self, columns, column_names)
        self.table.pack(fill="both", expand=True)

        ttk.Button(self, text="Обновить", command=self._load).pack(pady=5)
        self._load()

    def _load(self):
        try:
            enrollments = self.api._request("GET", "/api/enrollments/")
            all_topics = self.api._request("GET", "/api/topics/")
            
            try:
                students = self.api._request("GET", "/api/students/")
            except Exception:
                students = []
            try:
                teachers = self.api._request("GET", "/api/teachers/")
            except Exception:
                teachers = []
            all_users = students + teachers

            my_topic_ids = {
                t["id"] for t in all_topics if t.get("teacher_id") == self.teacher_id
            }
            user_map = {u["id"]: u for u in all_users}
            topic_map = {t["id"]: t for t in all_topics}

            result = []
            for e in enrollments:
                if e.get("topic_id") in my_topic_ids and e.get("status") in ("approved", "confirmed"):
                    student = user_map.get(e.get("student_id"), {})
                    topic = topic_map.get(e.get("topic_id"), {})
                    result.append({
                        "student_name": student.get("full_name", "?"),
                        "group_name": student.get("group_name", "?"),
                        "topic_title": topic.get("title", "?"),
                        "status": "✅ Подтверждено",
                    })

            self.table.set_data(result)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить студентов:\n{e}")


class RequestsFrame(ttk.Frame):
    def __init__(self, parent, api_client, teacher_id):
        super().__init__(parent)
        self.api = api_client
        self.teacher_id = teacher_id

        columns = ["id", "student_name", "topic_title", "status"]
        column_names = {
            "id": "ID",
            "student_name": "Студент",
            "topic_title": "Тема",
            "status": "Статус",
        }
        self.table = TableView(self, columns, column_names)
        self.table.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Одобрить", command=self._approve).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Отклонить", command=self._reject).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Обновить", command=self._load).pack(side="right", padx=2)

        self._load()

    def _load(self):
        try:
            enrollments = self.api._request("GET", "/api/enrollments/")
            all_topics = self.api._request("GET", "/api/topics/")
            
            try:
                students = self.api._request("GET", "/api/students/")
            except Exception:
                students = []
            try:
                teachers = self.api._request("GET", "/api/teachers/")
            except Exception:
                teachers = []
            all_users = students + teachers

            my_topic_ids = {
                t["id"] for t in all_topics if t.get("teacher_id") == self.teacher_id
            }
            user_map = {u["id"]: u.get("full_name", "?") for u in all_users}
            topic_map = {t["id"]: t.get("title", "?") for t in all_topics}

            result = []
            for e in enrollments:
                if e.get("topic_id") in my_topic_ids and e.get("status") == "pending":
                    result.append({
                        "id": e["id"],
                        "student_name": user_map.get(e.get("student_id"), "?"),
                        "topic_title": topic_map.get(e.get("topic_id"), "?"),
                        "status": "⏳ Ожидает",
                    })

            self.table.set_data(result)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить заявки:\n{e}")

    def _approve(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заявку")
            return
        try:
            self.api._request("PUT", f"/api/enrollments/{selected['id']}/confirm")
            messagebox.showinfo("Успех", "Заявка одобрена!")
            self._load()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _reject(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заявку")
            return
        try:
            self.api._request(
                "PUT",
                f"/api/enrollments/{selected['id']}/reject",
                json={"comment": "Отклонено преподавателем"}
            )
            messagebox.showinfo("Успех", "Заявка отклонена!")
            self._load()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))