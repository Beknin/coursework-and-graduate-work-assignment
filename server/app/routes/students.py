from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import User

router = APIRouter()


@router.get("/")
def get_students(db: Session = Depends(get_db)):
    return [s.to_dict() for s in User.get_students(db)]


@router.post("/api/students/")
def create_student(data: dict, db: Session = Depends(get_db)):
    full_name = data.get("full_name")
    if not full_name:
        raise HTTPException(status_code=400, detail="full_name обязателен")

    login = data.get("login") or full_name.lower().replace(" ", "_")
    existing = db.query(User).filter(User.login == login).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Логин '{login}' уже занят")

    student = User(
        full_name=full_name,
        login=login,
        role="student",
        email=data.get("email"),
        course=data.get("course", 1),
        group_name=data.get("group_name"),
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student.to_dict()


@router.put("/{student_id}")
def update_student(student_id: int, data: dict, db: Session = Depends(get_db)):
    student = User.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")

    if "login" in data and data["login"] != student.login:
        existing = db.query(User).filter(User.login == data["login"]).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Логин '{data['login']}' уже занят")

    updatable = ["full_name", "login", "email", "course", "group_name"]
    for field in updatable:
        if field in data:
            setattr(student, field, data[field])

    db.commit()
    db.refresh(student)
    return student.to_dict()


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = User.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    db.delete(student)
    db.commit()
    return {"status": "deleted"}