from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import User, Topic
from app.services.deadline_service import DeadlineChecker

router = APIRouter()


@router.get("/")
def get_topics(db: Session = Depends(get_db)):
    topics = db.query(Topic).all()
    return [
        t.to_dict(
            teacher_name=(db.query(User).get(t.teacher_id)).full_name
            if db.query(User).get(t.teacher_id) else None
        )
        for t in topics
    ]


@router.get("/free")
def get_free_topics(db: Session = Depends(get_db)):
    topics = db.query(Topic).filter(Topic.status == "free").all()
    return [
        t.to_dict(
            teacher_name=(db.query(User).get(t.teacher_id)).full_name
            if db.query(User).get(t.teacher_id) else None
        )
        for t in topics
    ]


@router.post("/")
def create_topic(topic_data: dict, db: Session = Depends(get_db)):
    if not DeadlineChecker.can_add_topic(db):
        raise HTTPException(status_code=403, detail="Дедлайн подачи тем истёк")

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
    )
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)

    return new_topic.to_dict(teacher_name=teacher.full_name)


@router.put("/{topic_id}")
def update_topic(topic_id: int, topic_data: dict, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")

    if "title" in topic_data:
        topic.title = topic_data["title"]
    if "level" in topic_data:
        topic.level = topic_data["level"]
    if "description" in topic_data:
        topic.description = topic_data["description"]
    if "teacher_id" in topic_data:
        teacher = User.get_teacher(db, topic_data["teacher_id"])
        if not teacher:
            raise HTTPException(status_code=404, detail="Преподаватель не найден")
        topic.teacher_id = topic_data["teacher_id"]

    db.commit()
    db.refresh(topic)

    teacher = db.query(User).get(topic.teacher_id)
    return topic.to_dict(teacher_name=teacher.full_name if teacher else None)


@router.delete("/{topic_id}")
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")
    db.delete(topic)
    db.commit()
    return {"status": "deleted"}