from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional
from app.models.models import Enrollment, Student, Topic
from app.utils.deadline_checker import DeadlineChecker


class EnrollmentController:
    """Контроллер для управления записями на темы"""

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_enrollments(self) -> List[dict]:
        """Получить все записи"""
        enrollments = self.db.query(Enrollment).all()
        return [
            {
                "id": e.id,
                "student_id": e.student_id,
                "student_name": e.student.full_name if e.student else "",
                "topic_id": e.topic_id,
                "topic_title": e.topic.title if e.topic else "",
                "status": e.status,
                "confirmed_at": e.confirmed_at.strftime("%d.%m.%Y") if e.confirmed_at else "—"
            }
            for e in enrollments
        ]

    def get_enrollments_by_student(self, student_id: int) -> List[dict]:
        """Получить записи конкретного студента"""
        enrollments = self.db.query(Enrollment).filter(Enrollment.student_id == student_id).all()
        return [
            {
                "id": e.id,
                "topic_id": e.topic_id,
                "topic_title": e.topic.title if e.topic else "",
                "status": e.status,
                "confirmed_at": e.confirmed_at.strftime("%d.%m.%Y") if e.confirmed_at else "—"
            }
            for e in enrollments
        ]

    def get_enrollments_by_teacher(self, teacher_id: int) -> List[dict]:
        """Получить записи на темы преподавателя"""
        enrollments = self.db.query(Enrollment).join(Topic).filter(
            Topic.teacher_id == teacher_id
        ).all()
        return [
            {
                "id": e.id,
                "student_name": e.student.full_name if e.student else "",
                "topic_title": e.topic.title if e.topic else "",
                "status": e.status
            }
            for e in enrollments
        ]

    def enroll_student(self, student_id: int, topic_id: int) -> dict:
        """Записать студента на тему"""
        # Проверяем дедлайн записи
        if not DeadlineChecker.can_enroll(self.db):
            raise ValueError("Период записи на темы закончился")
        
        # Проверяем, существует ли студент
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError(f"Студент с ID {student_id} не найден")
        
        # Проверяем, существует ли тема
        topic = self.db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise ValueError(f"Тема с ID {topic_id} не найдена")
        
        # Проверяем, не занята ли тема
        existing = self.db.query(Enrollment).filter(
            Enrollment.topic_id == topic_id,
            Enrollment.status == "confirmed"
        ).first()
        if existing:
            raise ValueError("Эта тема уже занята")
        
        # Проверяем, не записан ли студент уже на эту тему
        existing_student = self.db.query(Enrollment).filter(
            Enrollment.student_id == student_id,
            Enrollment.topic_id == topic_id
        ).first()
        if existing_student:
            raise ValueError("Вы уже записаны на эту тему")
        
        # Проверяем уровень (курс студента vs уровень темы)
        if topic.level == "ВКР" and student.course != 4:
            raise ValueError("На ВКР могут записываться только студенты 4-го курса")
        if topic.level == "Курсовая" and student.course not in [3, 4]:
            raise ValueError("Курсовая доступна для 3-го и 4-го курса")
        # "Курсовая/ВКР" подходит всем
        
        # Создаём запись
        enrollment = Enrollment(
            student_id=student_id,
            topic_id=topic_id,
            status="pending"
        )
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)
        
        return {
            "id": enrollment.id,
            "student_name": student.full_name,
            "topic_title": topic.title,
            "status": enrollment.status
        }

    def confirm_enrollment(self, enrollment_id: int) -> dict:
        """Подтвердить запись (преподаватель)"""
        enrollment = self.db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
        if not enrollment:
            raise ValueError(f"Запись с ID {enrollment_id} не найдена")
        
        if enrollment.status != "pending":
            raise ValueError(f"Запись уже {enrollment.status}")
        
        # Проверяем, не занята ли тема кем-то другим
        existing = self.db.query(Enrollment).filter(
            Enrollment.topic_id == enrollment.topic_id,
            Enrollment.status == "confirmed"
        ).first()
        if existing and existing.id != enrollment_id:
            raise ValueError("Эта тема уже занята другим студентом")
        
        enrollment.status = "confirmed"
        enrollment.confirmed_at = date.today()
        self.db.commit()
        self.db.refresh(enrollment)
        
        return {
            "id": enrollment.id,
            "status": enrollment.status,
            "confirmed_at": enrollment.confirmed_at.strftime("%d.%m.%Y")
        }

    def reject_enrollment(self, enrollment_id: int) -> dict:
        """Отклонить запись (преподаватель)"""
        enrollment = self.db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
        if not enrollment:
            raise ValueError(f"Запись с ID {enrollment_id} не найдена")
        
        if enrollment.status != "pending":
            raise ValueError(f"Запись уже {enrollment.status}")
        
        enrollment.status = "rejected"
        self.db.commit()
        
        return {
            "id": enrollment.id,
            "status": enrollment.status
        }