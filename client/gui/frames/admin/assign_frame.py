from tkinter import ttk, messagebox
import tkinter as tk
from gui.widgets.table_view import TableView
from api.enrollments_api import EnrollmentsAPI
from api.topics_api import TopicsAPI
from api.users_api import UsersAPI


class AssignFrame(ttk.Frame):
    def __init__(self, parent, api_client):
        super().__init__(parent)
        self.enroll_api = EnrollmentsAPI(api_client)
        self.topics_api = TopicsAPI(api_client)
        self.users_api = UsersAPI(api_client)

        manual_frame = ttk.LabelFrame(self, text="Назначение работ", padding=10)
        manual_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(manual_frame, text="Студент:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.student_var = tk.StringVar()
        self.student_combo = ttk.Combobox(
            manual_frame, textvariable=self.student_var, width=30, state="readonly"
        )
        self.student_combo.grid(row=0, column=1, padx=5, pady=5)

        # Тема
        ttk.Label(manual_frame, text="Тема:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.topic_var = tk.StringVar()
        self.topic_combo = ttk.Combobox(
            manual_frame, textvariable=self.topic_var, width=40, state="readonly"
        )
        self.topic_combo.grid(row=0, column=3, padx=5, pady=5)

        # Кнопка «Назначить»
        ttk.Button(manual_frame, text="Назначить", command=self._manual_assign).grid(
            row=0, column=4, padx=10, pady=5
        )

        table_frame = ttk.LabelFrame(self, text="История назначений", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ["id", "student_name", "topic_title", "status", "created_at"]
        column_names = {
            "id": "ID",
            "student_name": "Студент",
            "topic_title": "Тема",
            "status": "Статус",
            "created_at": "Дата",
        }
        self.table = TableView(table_frame, columns, column_names)
        self.table.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(table_frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Подтвердить", command=self._confirm).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Отклонить", command=self._reject).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Удалить", command=self._delete).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Обновить", command=self._load).pack(side="right", padx=2)

        self._load()

    def _load(self):
        try:
            enrollments = self.enroll_api.get_enrollments()
            status_map = {
                "pending": "Ожидает",
                "approved": "Подтверждено",
                "rejected": "Отклонено",
            }
            for e in enrollments:
                e["status"] = status_map.get(e.get("status"), e.get("status"))
            self.table.set_data(enrollments)

            all_students = self.users_api.get_all_users()
            students = [s for s in all_students if s.get("role") == "student"]
            assigned_ids = {
                e["student_id"] for e in enrollments
                if "Подтверждено" in e.get("status", "")
            }
            free_students = [s for s in students if s["id"] not in assigned_ids]
            self.student_ids = {
                f"{s['full_name']} (id={s['id']})": s["id"] for s in free_students
            }
            self.student_combo["values"] = list(self.student_ids.keys())

            free_topics = self.topics_api.get_free_topics()
            self.topic_ids = {
                f"{t['title']} (id={t['id']})": t["id"] for t in free_topics
            }
            self.topic_combo["values"] = list(self.topic_ids.keys())

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные:\n{e}")

    def _manual_assign(self):
        student_key = self.student_var.get()
        topic_key = self.topic_var.get()

        if not student_key or not topic_key:
            messagebox.showwarning("Предупреждение", "Выберите студента и тему")
            return

        student_id = self.student_ids.get(student_key)
        topic_id = self.topic_ids.get(topic_key)

        try:
            result = self.enroll_api.create_enrollment(student_id, topic_id)
            self.enroll_api.confirm_enrollment(result["id"])
            messagebox.showinfo("Успех", "Студент назначен на тему!")
            self.student_var.set("")
            self.topic_var.set("")
            self._load()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _confirm(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для подтверждения")
            return
        try:
            self.enroll_api.confirm_enrollment(selected["id"])
            self._load()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _reject(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для отклонения")
            return
        try:
            self.enroll_api.reject_enrollment(selected["id"], "Отклонено администратором")
            self._load()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _delete(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
            return
        if messagebox.askyesno("Подтверждение", "Удалить эту запись о назначении?"):
            try:
                self.enroll_api.delete_enrollment(selected["id"])
                self._load()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))