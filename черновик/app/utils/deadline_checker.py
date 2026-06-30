from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from app.models.models import Deadline


class DeadlineChecker:
    """Класс для проверки дедлайнов"""

    @staticmethod
    def get_deadline_date(db: Session, name: str) -> Optional[date]:
        """Получить дату дедлайна по имени"""
        deadline = db.query(Deadline).filter(
            Deadline.name == name,
            Deadline.is_active == 1
        ).first()
        return deadline.date if deadline else None

    @staticmethod
    def can_add_topic(db: Session) -> bool:
        """Можно ли добавлять темы (сентябрь)"""
        d = DeadlineChecker.get_deadline_date(db, "topics_start")
        if not d:
            return False
        return date.today() >= d

    @staticmethod
    def can_enroll(db: Session) -> bool:
        """Можно ли записываться (до ноября)"""
        d = DeadlineChecker.get_deadline_date(db, "enrollment_end")
        if not d:
            return False
        return date.today() <= d

    @staticmethod
    def can_change_topic(db: Session) -> bool:
        """Можно ли менять тему (до 15 февраля)"""
        d = DeadlineChecker.get_deadline_date(db, "change_deadline")
        if not d:
            return False
        return date.today() <= d

    @staticmethod
    def can_generate_preliminary_order(db: Session) -> bool:
        """Можно ли генерировать предварительный приказ (декабрь)"""
        d = DeadlineChecker.get_deadline_date(db, "preliminary_order")
        if not d:
            return False
        return date.today() >= d

    @staticmethod
    def can_generate_final_order(db: Session) -> bool:
        """Можно ли генерировать окончательный приказ (апрель)"""
        d = DeadlineChecker.get_deadline_date(db, "final_order")
        if not d:
            return False
        return date.today() >= d