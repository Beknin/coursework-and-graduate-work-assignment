from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database.db import get_db
from app.models import models
from app.schemas import schemas
from app.services.deadline_service import DeadlineChecker

router = APIRouter()


@router.post("/", response_model=schemas.EnrollmentResponse)
def enroll_student(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    if not DeadlineChecker.can_enroll(db):
        raise HTTPException(status_code=403, detail="Период записи закончился")
    
    student = db.query(models.Student).filter(models.Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    
    topic = db.query(models.Topic).filter(models.Topic.id == enrollment.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")
    
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.topic_id == enrollment.topic_id,
        models.Enrollment.status == "confirmed"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Тема уже занята")
    
    if topic.level == "ВКР" and student.course != 4:
        raise HTTPException(status_code=400, detail="На ВКР могут записываться только 4-й курс")
    
    if topic.level == "Курсовая" and student.course not in [3, 4]:
        raise HTTPException(status_code=400, detail="Курсовая доступна для 3-го и 4-го курса")
    
    existing_student = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.topic_id == enrollment.topic_id
    ).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Вы уже записаны на эту тему")
    
    db_enrollment = models.Enrollment(
        student_id=enrollment.student_id,
        topic_id=enrollment.topic_id,
        status="pending"
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    
    return schemas.EnrollmentResponse.model_validate(db_enrollment)


@router.put("/{enrollment_id}/confirm")
def confirm_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    
    if db_enrollment.status != "pending":
        raise HTTPException(status_code=400, detail=f"Запись уже {db_enrollment.status}")
    
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.topic_id == db_enrollment.topic_id,
        models.Enrollment.status == "confirmed"
    ).first()
    if existing and existing.id != enrollment_id:
        raise HTTPException(status_code=400, detail="Тема уже занята другим студентом")
    
    db_enrollment.status = "confirmed"
    db_enrollment.confirmed_at = date.today()
    db.commit()
    db.refresh(db_enrollment)
    
    return {"status": "confirmed", "id": enrollment_id}


@router.put("/{enrollment_id}/reject")
def reject_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    
    if db_enrollment.status != "pending":
        raise HTTPException(status_code=400, detail=f"Запись уже {db_enrollment.status}")
    
    db_enrollment.status = "rejected"
    db.commit()
    db.refresh(db_enrollment)
    
    return {"status": "rejected", "id": enrollment_id}
