from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from app.models import models


class DeadlineChecker:
    """Сервис для проверки дедлайнов"""

    @staticmethod
    def get_deadline_date(db: Session, name: str) -> Optional[date]:
        """Получить дату дедлайна по имени"""
        deadline = db.query(models.Deadline).filter(
            models.Deadline.name == name,
            models.Deadline.is_active == 1
        ).first()
        return deadline.date if deadline else None

    @staticmethod
    def can_add_topic(db: Session) -> bool:
        d = DeadlineChecker.get_deadline_date(db, "topics_start")
        return date.today() >= d if d else False

    @staticmethod
    def can_enroll(db: Session) -> bool:
        d = DeadlineChecker.get_deadline_date(db, "enrollment_end")
        return date.today() <= d if d else False

    @staticmethod
    def can_change_topic(db: Session) -> bool:
        d = DeadlineChecker.get_deadline_date(db, "change_deadline")
        return date.today() <= d if d else False

    @staticmethod
    def can_generate_preliminary_order(db: Session) -> bool:
        d = DeadlineChecker.get_deadline_date(db, "preliminary_order")
        return date.today() >= d if d else False

    @staticmethod
    def can_generate_final_order(db: Session) -> bool:
        d = DeadlineChecker.get_deadline_date(db, "final_order")
        return date.today() >= d if d else False