from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.models import models
from app.schemas import schemas
from app.services.deadline_service import DeadlineChecker

router = APIRouter()


@router.get("/", response_model=List[schemas.TopicResponse])
def get_topics(db: Session = Depends(get_db)):
    """Получить все темы"""
    topics = db.query(models.Topic).all()
    
    result = []
    for topic in topics:
        # Проверяем, занята ли тема
        is_taken = db.query(models.Enrollment).filter(
            models.Enrollment.topic_id == topic.id,
            models.Enrollment.status == "confirmed"
        ).first() is not None
        
        topic_data = schemas.TopicResponse.model_validate(topic)
        topic_data.status = "taken" if is_taken else "free"
        result.append(topic_data)
    
    return result


@router.post("/", response_model=schemas.TopicResponse)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    """Создать новую тему (только преподаватель)"""
    # Проверка дедлайна
    if not DeadlineChecker.can_add_topic(db):
        raise HTTPException(status_code=403, detail="Период ввода тем закончился")
    
    # Проверяем преподавателя
    teacher = db.query(models.Teacher).filter(models.Teacher.id == topic.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")
    
    # Создаём тему
    from datetime import date
    db_topic = models.Topic(
        teacher_id=topic.teacher_id,
        level=topic.level,
        title=topic.title,
        description=topic.description,
        created_at=date.today()
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    
    return schemas.TopicResponse.model_validate(db_topic)


@router.get("/free", response_model=List[schemas.TopicResponse])
def get_free_topics(db: Session = Depends(get_db)):
    """Получить свободные темы (без подтверждённых записей)"""
    # ID тем, на которые есть подтверждённые записи
    taken_ids = db.query(models.Enrollment.topic_id).filter(
        models.Enrollment.status == "confirmed"
    ).subquery()
    
    free_topics = db.query(models.Topic).filter(
        models.Topic.id.notin_(taken_ids)
    ).all()
    
    result = []
    for topic in free_topics:
        topic_data = schemas.TopicResponse.model_validate(topic)
        topic_data.status = "free"
        result.append(topic_data)
    
    return result


@router.put("/{topic_id}")
def update_topic(topic_id: int, topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    """Изменить тему (только преподаватель с разрешения админа)"""
    if not DeadlineChecker.can_change_topic(db):
        raise HTTPException(status_code=403, detail="Период изменения тем закончился")
    
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")
    
    db_topic.teacher_id = topic.teacher_id
    db_topic.level = topic.level
    db_topic.title = topic.title
    db_topic.description = topic.description
    
    db.commit()
    db.refresh(db_topic)
    
    return {"status": "updated", "id": topic_id}


@router.delete("/{topic_id}")
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    """Удалить тему (только админ)"""
    # Проверяем, есть ли записи
    count = db.query(models.Enrollment).filter(models.Enrollment.topic_id == topic_id).count()
    if count > 0:
        raise HTTPException(status_code=400, detail="Нельзя удалить тему с записями")
    
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")
    
    db.delete(db_topic)
    db.commit()
    
    return {"status": "deleted"}