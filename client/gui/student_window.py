from tkinter import ttk, messagebox
import tkinter as tk
from gui.app import App
from gui.widgets.table_view import TableView
from gui.widgets.status_bar import StatusBar


class StudentWindow(App):
    def __init__(self, user, api_client):
        super().__init__(f"Студент: {user.get('full_name', '')}", user, api_client)

    def _create_widgets(self):
        header = ttk.Frame(self.window)
        header.pack(fill="x", padx=10, pady=5)
        ttk.Label(header, text=f"{self.user.get('full_name', '')} (студент)",
                  font=("Arial", 11)).pack(side="left")
        ttk.Button(header, text="Выйти", command=self.on_close).pack(side="right")

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.available_frame = AvailableTopicsFrame(notebook, self.api, self.user)
        notebook.add(self.available_frame, text="Доступные темы")

        self.my_choice_frame = MyChoiceFrame(notebook, self.api, self.user)
        notebook.add(self.my_choice_frame, text="Мой выбор")

        self.status_bar = StatusBar(self.window)
        self.status_bar.set_status(f"Студент | {self.user.get('group_name', '')}")


class AvailableTopicsFrame(ttk.Frame):
    def __init__(self, parent, api_client, user):
        super().__init__(parent)
        self.api = api_client
        self.user = user

        columns = ["id", "title", "level", "teacher_name", "description"]
        column_names = {
            "id": "ID", "title": "Название", "level": "Тип",
            "teacher_name": "Преподаватель", "description": "Описание"
        }
        self.table = TableView(self, columns, column_names)
        self.table.pack(fill="both", expand=True)

        ttk.Button(self, text="Подать заявку", command=self._apply).pack(pady=10)
        ttk.Button(self, text="Обновить", command=self._load).pack(pady=5)

        self._load()

    def _load(self):
        try:
            free_topics = self.api._request("GET", "/api/topics/free")
            for t in free_topics:
                t["level"] = "Курсовая" if t.get("level") == "coursework" else "Диплом"
            self.table.set_data(free_topics)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _apply(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите тему")
            return
        try:
            self.api._request("POST", "/api/enrollments/", json={
                "student_id": self.user["id"],
                "topic_id": selected["id"],
            })
            messagebox.showinfo("Успех", "Заявка подана! Ожидайте подтверждения.")
            self._load()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


class MyChoiceFrame(ttk.Frame):
    def __init__(self, parent, api_client, user):
        super().__init__(parent)
        self.api = api_client
        self.user = user

        self.info_label = ttk.Label(self, text="Загрузка...", font=("Arial", 12))
        self.info_label.pack(pady=30)

        self.cancel_btn = ttk.Button(self, text="❌ Отозвать заявку", command=self._cancel)
        self.cancel_btn.pack(pady=10)

        ttk.Button(self, text="🔄 Обновить", command=self._load).pack(pady=10)

        self._load()

    def _load(self):
        try:
            enrollments = self.api._request("GET", "/api/enrollments/")
            my_enrollment = next(
                (e for e in enrollments if e.get("student_id") == self.user["id"]),
                None
            )

            if not my_enrollment:
                self.info_label.config(text="📭 У вас пока нет выбранной темы.\nПерейдите на вкладку «Доступные темы».")
                self.cancel_btn.pack_forget()
                return

            topic = self.api._request("GET", "/api/topics/")
            topic = next((t for t in topic if t["id"] == my_enrollment.get("topic_id")), {})

            status_text = {
                "pending": "⏳ Ожидает подтверждения",
                "approved": "✅ Подтверждено",
                "rejected": "❌ Отклонено",
            }.get(my_enrollment.get("status"), my_enrollment.get("status"))

            self.info_label.config(text=(
                f"Тема: {topic.get('title', '?')}\n"
                f"Тип: {'Курсовая' if topic.get('level') == 'coursework' else 'Диплом'}\n"
                f"Преподаватель: {topic.get('teacher_name', '?')}\n"
                f"Статус: {status_text}"
            ))

            if my_enrollment.get("status") == "pending":
                self.cancel_btn.pack()
            else:
                self.cancel_btn.pack_forget()

        except Exception as e:
            self.info_label.config(text=f"Ошибка: {e}")

    def _cancel(self):
        if messagebox.askyesno("Подтверждение", "Отозвать заявку?"):
            try:
                enrollments = self.api._request("GET", "/api/enrollments/")
                my_enrollment = next(
                    (e for e in enrollments if e.get("student_id") == self.user["id"]),
                    None
                )
                if my_enrollment:
                    self.api._request("DELETE", f"/api/enrollments/{my_enrollment['id']}")
                    self._load()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))