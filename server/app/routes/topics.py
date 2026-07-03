from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database.db import get_db
from app.models.models import User, Topic, Enrollment
from app.services.deadline_service import DeadlineChecker

router = APIRouter()


@router.get("/")
def get_topics(db: Session = Depends(get_db)):
    topics = db.query(Topic).all()
    result = []
    for t in topics:
        teacher = db.query(User).get(t.teacher_id)
        topic_dict = t.to_dict(
            teacher_name=teacher.full_name if teacher else "Неизвестный"
        )
        is_taken = db.query(Enrollment).filter(
            Enrollment.topic_id == t.id,
            Enrollment.status == "confirmed"
        ).first() is not None
        topic_dict["status"] = "taken" if is_taken else (t.status or "free")
        result.append(topic_dict)
    return result


@router.get("/free")
def get_free_topics(db: Session = Depends(get_db)):
    taken_ids = db.query(Enrollment.topic_id).filter(
        Enrollment.status == "confirmed"
    ).subquery()
    
    free_topics = db.query(Topic).filter(
        Topic.id.notin_(taken_ids)
    ).all()
    
    result = []
    for t in free_topics:
        teacher = db.query(User).get(t.teacher_id)
        result.append(t.to_dict(
            teacher_name=teacher.full_name if teacher else "Неизвестный"
        ))
    return result


@router.get("/teacher/{teacher_id}")
def get_topics_by_teacher(teacher_id: int, db: Session = Depends(get_db)):
    topics = db.query(Topic).filter(Topic.teacher_id == teacher_id).all()
    result = []
    for t in topics:
        teacher = db.query(User).get(teacher_id)
        result.append(t.to_dict(
            teacher_name=teacher.full_name if teacher else "Неизвестный"
        ))
    return result


@router.post("/")
def create_topic(topic_data: dict, db: Session = Depends(get_db)):
    if not DeadlineChecker.can_add_topic(db):
        raise HTTPException(status_code=403, detail="Период ввода тем закончился")

    teacher_id = topic_data.get("teacher_id")
    teacher = User.get_teacher(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")

    new_topic = Topic(
        teacher_id=teacher_id,
        level=topic_data.get("level", "coursework"),
        title=topic_data.get("title"),
        description=topic_data.get("description"),
        status="free",
        created_at=date.today(),
    )
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)

    return new_topic.to_dict(teacher_name=teacher.full_name)


@router.put("/{topic_id}")
def update_topic(topic_id: int, topic_data: dict, db: Session = Depends(get_db)):
    if not DeadlineChecker.can_change_topic(db):
        raise HTTPException(status_code=403, detail="Период изменения тем закончился")

    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")

    if "title" in topic_data:
        db_topic.title = topic_data["title"]
    if "level" in topic_data:
        db_topic.level = topic_data["level"]
    if "description" in topic_data:
        db_topic.description = topic_data["description"]
    if "teacher_id" in topic_data:
        teacher = User.get_teacher(db, topic_data["teacher_id"])
        if not teacher:
            raise HTTPException(status_code=404, detail="Преподаватель не найден")
        db_topic.teacher_id = topic_data["teacher_id"]

    db.commit()
    db.refresh(db_topic)

    teacher = db.query(User).get(db_topic.teacher_id)
    return db_topic.to_dict(teacher_name=teacher.full_name if teacher else None)


@router.delete("/{topic_id}")
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    count = db.query(Enrollment).filter(Enrollment.topic_id == topic_id).count()
    if count > 0:
        raise HTTPException(status_code=400, detail="Нельзя удалить тему с записями")

    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")

    db.delete(db_topic)
    db.commit()
    return {"status": "deleted"}