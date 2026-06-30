from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Dict

from app.database.db import get_db
from app.models import models
from app.services.order_service import OrderService
from app.services.deadline_service import DeadlineChecker

router = APIRouter()


@router.get("/preliminary")
def generate_preliminary_order(db: Session = Depends(get_db)):
    """Сгенерировать предварительный приказ (декабрь)"""
    if not DeadlineChecker.can_generate_preliminary_order(db):
        raise HTTPException(status_code=403, detail="Дедлайн для генерации приказа ещё не наступил")
    
    data = _get_order_data(db)
    file_path = OrderService.generate_order(data, "preliminary")
    return FileResponse(file_path, filename="preliminary_order.docx")


@router.get("/final")
def generate_final_order(db: Session = Depends(get_db)):
    """Сгенерировать окончательный приказ (апрель)"""
    if not DeadlineChecker.can_generate_final_order(db):
        raise HTTPException(status_code=403, detail="Дедлайн для генерации приказа ещё не наступил")
    
    data = _get_order_data(db)
    file_path = OrderService.generate_order(data, "final")
    return FileResponse(file_path, filename="final_order.docx")


def _get_order_data(db: Session) -> List[Dict]:
    """Получить данные для приказа"""
    query = """
        SELECT s.full_name, s.course, s.group_name,
               t.title as topic_title, t.level,
               tf.full_name as teacher_name
        FROM students s
        LEFT JOIN enrollments e ON s.id = e.student_id AND e.status = 'confirmed'
        LEFT JOIN topics t ON e.topic_id = t.id
        LEFT JOIN teachers tf ON t.teacher_id = tf.id
        ORDER BY s.full_name
    """
    result = db.execute(query).fetchall()
    
    return [
        {
            "student_name": row[0],
            "course": row[1],
            "group": row[2],
            "topic_title": row[3] or "—",
            "teacher_name": row[5] or "—"
        }
        for row in result
    ]