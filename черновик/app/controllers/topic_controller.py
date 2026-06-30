from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional
from app.models.models import Topic, Teacher, Enrollment
from app.utils.deadline_checker import DeadlineChecker


class TopicController:
    """Контроллер для управления темами"""

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_topics(self) -> List[dict]:
        """Получить все темы с дополнительной информацией"""
        topics = self.db.query(Topic).all()
        result = []
        for topic in topics:
            # Проверяем, занята ли тема
            is_taken = self.db.query(Enrollment).filter(
                Enrollment.topic_id == topic.id,
                Enrollment.status == "confirmed"
            ).first() is not None
            
            result.append({
                "id": topic.id,
                "title": topic.title,
                "level": topic.level,
                "description": topic.description,
                "teacher_id": topic.teacher_id,
                "teacher_name": topic.teacher.full_name if topic.teacher else "Не указан",
                "created_at": topic.created_at.strftime("%d.%m.%Y") if topic.created_at else "",
                "is_taken": is_taken,
                "status": "Занята" if is_taken else "Свободна"
            })
        return result

    def get_free_topics(self) -> List[dict]:
        """Получить только свободные темы"""
        # Находим ID тем, на которые есть подтверждённые записи
        taken_topic_ids = self.db.query(Enrollment.topic_id).filter(
            Enrollment.status == "confirmed"
        ).subquery()
        
        free_topics = self.db.query(Topic).filter(
            Topic.id.notin_(taken_topic_ids)
        ).all()
        
        return [
            {
                "id": t.id,
                "title": t.title,
                "level": t.level,
                "teacher_name": t.teacher.full_name if t.teacher else "Не указан",
                "description": t.description
            }
            for t in free_topics
        ]

    def get_topics_by_teacher(self, teacher_id: int) -> List[dict]:
        """Получить темы конкретного преподавателя"""
        topics = self.db.query(Topic).filter(Topic.teacher_id == teacher_id).all()
        return [
            {
                "id": t.id,
                "title": t.title,
                "level": t.level,
                "created_at": t.created_at.strftime("%d.%m.%Y") if t.created_at else ""
            }
            for t in topics
        ]

    def create_topic(self, teacher_id: int, level: str, title: str, description: str = "") -> dict:
        """Создать новую тему"""
        # Проверяем дедлайн
        if not DeadlineChecker.can_add_topic(self.db):
            raise ValueError("Период ввода тем закончился")
        
        # Проверяем преподавателя
        teacher = self.db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise ValueError(f"Преподаватель с ID {teacher_id} не найден")
        
        # Создаём тему
        new_topic = Topic(
            teacher_id=teacher_id,
            level=level,
            title=title,
            description=description,
            created_at=date.today()
        )
        self.db.add(new_topic)
        self.db.commit()
        self.db.refresh(new_topic)
        
        return {
            "id": new_topic.id,
            "title": new_topic.title,
            "level": new_topic.level,
            "teacher_name": teacher.full_name,
            "created_at": new_topic.created_at.strftime("%d.%m.%Y")
        }

    def update_topic(self, topic_id: int, title: str = None, level: str = None, description: str = None) -> dict:
        """Обновить тему"""
        topic = self.db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise ValueError(f"Тема с ID {topic_id} не найдена")
        
        # Проверяем дедлайн (смену темы можно только до определённой даты)
        if not DeadlineChecker.can_change_topic(self.db):
            raise ValueError("Период изменения тем закончился")
        
        if title is not None:
            topic.title = title
        if level is not None:
            topic.level = level
        if description is not None:
            topic.description = description
        
        self.db.commit()
        self.db.refresh(topic)
        
        return {
            "id": topic.id,
            "title": topic.title,
            "level": topic.level,
            "updated": True
        }

    def delete_topic(self, topic_id: int) -> bool:
        """Удалить тему (только админ)"""
        # Проверяем, есть ли записи на эту тему
        enrollments = self.db.query(Enrollment).filter(Enrollment.topic_id == topic_id).count()
        if enrollments > 0:
            raise ValueError("Нельзя удалить тему, на которую уже есть записи")
        
        topic = self.db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise ValueError(f"Тема с ID {topic_id} не найдена")
        
        self.db.delete(topic)
        self.db.commit()
        return True