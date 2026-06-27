from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.models import Teacher


class TeacherController:
    """Контроллер для управления преподавателями"""

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_teachers(self) -> List[dict]:
        """Получить всех преподавателей"""
        teachers = self.db.query(Teacher).all()
        return [
            {
                "id": t.id,
                "full_name": t.full_name,
                "position": t.position,
                "degree": t.degree,
                "contact": t.contact
            }
            for t in teachers
        ]

    def get_teacher_by_id(self, teacher_id: int) -> dict:
        """Получить преподавателя по ID"""
        teacher = self.db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise ValueError(f"Преподаватель с ID {teacher_id} не найден")
        return {
            "id": teacher.id,
            "full_name": teacher.full_name,
            "position": teacher.position,
            "degree": teacher.degree,
            "contact": teacher.contact
        }

    def create_teacher(self, full_name: str, position: str = "", degree: str = "", contact: str = "") -> dict:
        """Добавить преподавателя"""
        teacher = Teacher(
            full_name=full_name,
            position=position,
            degree=degree,
            contact=contact
        )
        self.db.add(teacher)
        self.db.commit()
        self.db.refresh(teacher)
        
        return {
            "id": teacher.id,
            "full_name": teacher.full_name,
            "position": teacher.position,
            "degree": teacher.degree,
            "contact": teacher.contact
        }

    def update_teacher(self, teacher_id: int, full_name: str = None, position: str = None, degree: str = None, contact: str = None) -> dict:
        """Обновить данные преподавателя"""
        teacher = self.db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise ValueError(f"Преподаватель с ID {teacher_id} не найден")
        
        if full_name is not None:
            teacher.full_name = full_name
        if position is not None:
            teacher.position = position
        if degree is not None:
            teacher.degree = degree
        if contact is not None:
            teacher.contact = contact
        
        self.db.commit()
        self.db.refresh(teacher)
        
        return {
            "id": teacher.id,
            "full_name": teacher.full_name,
            "position": teacher.position,
            "degree": teacher.degree,
            "contact": teacher.contact
        }

    def delete_teacher(self, teacher_id: int) -> bool:
        """Удалить преподавателя"""
        teacher = self.db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise ValueError(f"Преподаватель с ID {teacher_id} не найден")
        
        # Проверяем, есть ли темы
        from app.models.models import Topic
        topics = self.db.query(Topic).filter(Topic.teacher_id == teacher_id).count()
        if topics > 0:
            raise ValueError("Нельзя удалить преподавателя с активными темами")
        
        self.db.delete(teacher)
        self.db.commit()
        return True