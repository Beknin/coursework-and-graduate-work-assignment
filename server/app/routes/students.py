from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


@router.post("/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    if student.course not in [3, 4]:
        raise HTTPException(status_code=400, detail="Курс должен быть 3 или 4")
    
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.put("/{student_id}")
def update_student(student_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    
    for key, value in student.model_dump().items():
        setattr(db_student, key, value)
    
    db.commit()
    db.refresh(db_student)
    return {"status": "updated"}


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    count = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == student_id
    ).count()
    if count > 0:
        raise HTTPException(status_code=400, detail="Нельзя удалить студента с записями")
    
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    
    db.delete(db_student)
    db.commit()
    return {"status": "deleted"}