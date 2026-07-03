import tkinter as tk
from tkinter import ttk


class TopicDialog(tk.Toplevel):
    def __init__(self, parent, topic: dict = None, teachers: list = None):
        super().__init__(parent)
        self.result = None
        self.title("Редактировать тему" if topic else "Добавить тему")
        self.geometry("400x350")
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Название:").grid(row=0, column=0, sticky="e", pady=5)
        self.title_entry = ttk.Entry(frame, width=35)
        self.title_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Тип:").grid(row=1, column=0, sticky="e", pady=5)
        self.level = ttk.Combobox(frame, values=["coursework", "diploma"], width=33)
        self.level.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Преподаватель:").grid(row=2, column=0, sticky="e", pady=5)
        self.teacher_var = tk.StringVar()
        self.teacher_combo = ttk.Combobox(frame, textvariable=self.teacher_var, width=33)
        if teachers:
            self.teacher_list = [f"{t['full_name']} (id={t['id']})" for t in teachers]
            self.teacher_ids = {f"{t['full_name']} (id={t['id']})": t['id'] for t in teachers}
            self.teacher_combo['values'] = self.teacher_list
        self.teacher_combo.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Описание:").grid(row=3, column=0, sticky="ne", pady=5)
        self.description = tk.Text(frame, width=35, height=5)
        self.description.grid(row=3, column=1, pady=5)

        if topic:
            self.title_entry.insert(0, topic.get("title", ""))
            self.level.set(topic.get("level", ""))
            self.description.insert("1.0", topic.get("description", ""))
            if teachers:
                for t in teachers:
                    if t['id'] == topic.get('teacher_id'):
                        self.teacher_var.set(f"{t['full_name']} (id={t['id']})")
                        break

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Сохранить", command=self._on_save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.destroy).pack(side="left", padx=5)

        self.grab_set()
        self.wait_window()

    def _on_save(self):
        teacher_str = self.teacher_var.get()
        teacher_id = None
        if hasattr(self, 'teacher_ids') and teacher_str in self.teacher_ids:
            teacher_id = self.teacher_ids[teacher_str]

        self.result = {
            "title": self.title_entry.get().strip(),
            "level": self.level.get(),
            "teacher_id": teacher_id,
            "description": self.description.get("1.0", "end-1c").strip(),
        }
        self.destroy()