from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database.db import get_db
from app.models.models import User, Topic, Enrollment
from app.services.deadline_service import DeadlineChecker

router = APIRouter()


@router.get("/api/enrollments/")
def get_enrollments(db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).all()
    result = []
    for e in enrollments:
        student = db.query(User).get(e.student_id)
        topic = db.query(Topic).get(e.topic_id)
        result.append(e.to_dict(
            student_name=student.full_name if student else None,
            topic_title=topic.title if topic else None,
        ))
    return result


@router.post("/api/enrollments/")
def create_enrollment(data: dict, db: Session = Depends(get_db)):
    if not DeadlineChecker.can_enroll(db):
        raise HTTPException(status_code=403, detail="Запись на темы закрыта по дедлайну")

    student_id = data.get("student_id")
    topic_id = data.get("topic_id")

    student = User.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")

    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")

    if topic.status != "free":
        raise HTTPException(status_code=400, detail="Тема уже занята")

    existing = db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.topic_id == topic_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Вы уже подали заявку на эту тему")

    has_approved = db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.status == "approved",
    ).first()
    if has_approved:
        raise HTTPException(status_code=400, detail="У вас уже есть назначенная тема")

    enrollment = Enrollment(
        student_id=student_id,
        topic_id=topic_id,
        status="pending",
        created_at=date.today(),
    )
    db.add(enrollment)

    topic.status = "reserved"

    db.commit()
    db.refresh(enrollment)

    return enrollment.to_dict(
        student_name=student.full_name,
        topic_title=topic.title,
    )


@router.put("/api/enrollments/{enrollment_id}/confirm")
def confirm_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    if enrollment.status != "pending":
        raise HTTPException(status_code=400, detail="Можно подтвердить только ожидающую заявку")

    enrollment.status = "approved"
    enrollment.confirmed_at = date.today()

    topic = db.query(Topic).get(enrollment.topic_id)
    if topic:
        topic.status = "assigned"

    other_enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.id != enrollment_id,
        Enrollment.status == "pending",
    ).all()
    for e in other_enrollments:
        e.status = "rejected"
        e.comment = "Студент выбрал другую тему"

    db.commit()
    db.refresh(enrollment)

    student = db.query(User).get(enrollment.student_id)
    topic = db.query(Topic).get(enrollment.topic_id)
    return enrollment.to_dict(
        student_name=student.full_name if student else None,
        topic_title=topic.title if topic else None,
    )


@router.put("/api/enrollments/{enrollment_id}/reject")
def reject_enrollment(enrollment_id: int, data: dict = None, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    if enrollment.status not in ["pending", "approved"]:
        raise HTTPException(status_code=400, detail="Нельзя отклонить эту заявку")

    enrollment.status = "rejected"
    enrollment.comment = data.get("comment") if data else None

    topic = db.query(Topic).get(enrollment.topic_id)
    if topic and topic.status == "assigned":
        other_approved = db.query(Enrollment).filter(
            Enrollment.topic_id == enrollment.topic_id,
            Enrollment.id != enrollment_id,
            Enrollment.status == "approved",
        ).first()
        if not other_approved:
            topic.status = "free"

    db.commit()
    db.refresh(enrollment)

    student = db.query(User).get(enrollment.student_id)
    topic = db.query(Topic).get(enrollment.topic_id)
    return enrollment.to_dict(
        student_name=student.full_name if student else None,
        topic_title=topic.title if topic else None,
    )


@router.delete("/api/enrollments/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    topic = db.query(Topic).get(enrollment.topic_id)
    if topic and topic.status in ["assigned", "reserved"]:
        other_approved = db.query(Enrollment).filter(
            Enrollment.topic_id == enrollment.topic_id,
            Enrollment.id != enrollment_id,
            Enrollment.status == "approved",
        ).first()
        if not other_approved:
            topic.status = "free"

    db.delete(enrollment)
    db.commit()
    return {"status": "deleted"}