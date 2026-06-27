from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.models import Student


class StudentController:
    """Контроллер для управления студентами"""

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_students(self) -> List[dict]:
        """Получить всех студентов"""
        students = self.db.query(Student).all()
        return [
            {
                "id": s.id,
                "full_name": s.full_name,
                "course": s.course,
                "group_name": s.group_name
            }
            for s in students
        ]

    def get_student_by_id(self, student_id: int) -> dict:
        """Получить студента по ID"""
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError(f"Студент с ID {student_id} не найден")
        return {
            "id": student.id,
            "full_name": student.full_name,
            "course": student.course,
            "group_name": student.group_name
        }

    def create_student(self, full_name: str, course: int, group_name: str = "") -> dict:
        """Добавить студента"""
        if course not in [3, 4]:
            raise ValueError("Курс должен быть 3 или 4")
        
        student = Student(
            full_name=full_name,
            course=course,
            group_name=group_name
        )
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        
        return {
            "id": student.id,
            "full_name": student.full_name,
            "course": student.course,
            "group_name": student.group_name
        }

    def update_student(self, student_id: int, full_name: str = None, course: int = None, group_name: str = None) -> dict:
        """Обновить данные студента"""
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError(f"Студент с ID {student_id} не найден")
        
        if full_name is not None:
            student.full_name = full_name
        if course is not None:
            if course not in [3, 4]:
                raise ValueError("Курс должен быть 3 или 4")
            student.course = course
        if group_name is not None:
            student.group_name = group_name
        
        self.db.commit()
        self.db.refresh(student)
        
        return {
            "id": student.id,
            "full_name": student.full_name,
            "course": student.course,
            "group_name": student.group_name
        }

    def delete_student(self, student_id: int) -> bool:
        """Удалить студента"""
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError(f"Студент с ID {student_id} не найден")
        
        # Проверяем, есть ли активные записи
        from app.models.models import Enrollment
        enrollments = self.db.query(Enrollment).filter(
            Enrollment.student_id == student_id
        ).count()
        if enrollments > 0:
            raise ValueError("Нельзя удалить студента с активными записями")
        
        self.db.delete(student)
        self.db.commit()
        return True

    def get_students_by_course(self, course: int) -> List[dict]:
        """Получить студентов по курсу"""
        students = self.db.query(Student).filter(Student.course == course).all()
        return [
            {
                "id": s.id,
                "full_name": s.full_name,
                "group_name": s.group_name
            }
            for s in students
        ]