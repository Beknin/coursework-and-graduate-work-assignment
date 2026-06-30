from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional
from app.models.models import Deadline


class DeadlineController:
    """Контроллер для управления дедлайнами"""

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_deadlines(self) -> List[dict]:
        """Получить все дедлайны"""
        deadlines = self.db.query(Deadline).all()
        return [
            {
                "id": d.id,
                "name": d.name,
                "date": d.date.strftime("%d.%m.%Y"),
                "is_active": bool(d.is_active)
            }
            for d in deadlines
        ]

    def get_deadline_by_name(self, name: str) -> Optional[dict]:
        """Получить дедлайн по имени"""
        deadline = self.db.query(Deadline).filter(
            Deadline.name == name,
            Deadline.is_active == 1
        ).first()
        if not deadline:
            return None
        return {
            "id": deadline.id,
            "name": deadline.name,
            "date": deadline.date.strftime("%d.%m.%Y")
        }

    def create_deadline(self, name: str, date_str: str, is_active: bool = True) -> dict:
        """Создать дедлайн"""
        from datetime import datetime
        try:
            deadline_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте YYYY-MM-DD")
        
        deadline = Deadline(
            name=name,
            date=deadline_date,
            is_active=1 if is_active else 0
        )
        self.db.add(deadline)
        self.db.commit()
        self.db.refresh(deadline)
        
        return {
            "id": deadline.id,
            "name": deadline.name,
            "date": deadline.date.strftime("%d.%m.%Y"),
            "is_active": bool(deadline.is_active)
        }

    def update_deadline(self, deadline_id: int, date_str: str = None, is_active: bool = None) -> dict:
        """Обновить дедлайн"""
        deadline = self.db.query(Deadline).filter(Deadline.id == deadline_id).first()
        if not deadline:
            raise ValueError(f"Дедлайн с ID {deadline_id} не найден")
        
        if date_str is not None:
            from datetime import datetime
            try:
                deadline.date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Неверный формат даты. Используйте YYYY-MM-DD")
        
        if is_active is not None:
            deadline.is_active = 1 if is_active else 0
        
        self.db.commit()
        self.db.refresh(deadline)
        
        return {
            "id": deadline.id,
            "name": deadline.name,
            "date": deadline.date.strftime("%d.%m.%Y"),
            "is_active": bool(deadline.is_active)
        }