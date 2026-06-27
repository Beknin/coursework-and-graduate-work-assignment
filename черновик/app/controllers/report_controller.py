from sqlalchemy.orm import Session
from datetime import date
from typing import List, Dict
from app.models.models import Student, Teacher, Topic, Enrollment
from app.utils.word_generator import WordGenerator


class ReportController:
    """Контроллер для генерации отчётов и приказов"""

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_preliminary_order_data(self) -> Dict:
        """Получить данные для предварительного приказа (декабрь)"""
        students = self.db.query(Student).all()
        result = []
        for student in students:
            enrollment = self.db.query(Enrollment).filter(
                Enrollment.student_id == student.id,
                Enrollment.status == "confirmed"
            ).first()
            result.append({
                "student_name": student.full_name,
                "course": student.course,
                "group": student.group_name,
                "topic_title": enrollment.topic.title if enrollment else "—",
                "teacher_name": enrollment.topic.teacher.full_name if enrollment and enrollment.topic and enrollment.topic.teacher else "—"
            })
        return {
            "order_type": "ПРЕДВАРИТЕЛЬНЫЙ",
            "date": date.today().strftime("%d.%m.%Y"),
            "students": result
        }

    def get_final_order_data(self) -> Dict:
        """Получить данные для окончательного приказа (апрель)"""
        enrollments = self.db.query(Enrollment).filter(
            Enrollment.status == "confirmed"
        ).all()
        result = []
        for e in enrollments:
            result.append({
                "student_name": e.student.full_name if e.student else "—",
                "course": e.student.course if e.student else "—",
                "group": e.student.group_name if e.student else "—",
                "topic_title": e.topic.title if e.topic else "—",
                "level": e.topic.level if e.topic else "—",
                "teacher_name": e.topic.teacher.full_name if e.topic and e.topic.teacher else "—"
            })
        return {
            "order_type": "ОКОНЧАТЕЛЬНЫЙ",
            "date": date.today().strftime("%d.%m.%Y"),
            "students": result
        }

    def generate_preliminary_order(self, output_path: str = None) -> str:
        """Сгенерировать предварительный приказ в Word"""
        data = self.get_preliminary_order_data()
        if output_path is None:
            output_path = f"preliminary_order_{date.today().strftime('%Y%m%d')}.docx"
        return WordGenerator.generate_order(data, output_path)

    def generate_final_order(self, output_path: str = None) -> str:
        """Сгенерировать окончательный приказ в Word"""
        data = self.get_final_order_data()
        if output_path is None:
            output_path = f"final_order_{date.today().strftime('%Y%m%d')}.docx"
        return WordGenerator.generate_order(data, output_path)