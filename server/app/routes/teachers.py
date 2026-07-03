from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import User

router = APIRouter()


@router.get("/")
def get_teachers(db: Session = Depends(get_db)):
    return [t.to_dict() for t in User.get_teachers(db)]


@router.post("/")
def create_teacher(data: dict, db: Session = Depends(get_db)):
    full_name = data.get("full_name")
    if not full_name:
        raise HTTPException(status_code=400, detail="full_name обязателен")

    login = data.get("login") or full_name.lower().replace(" ", "_")
    existing = db.query(User).filter(User.login == login).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Логин '{login}' уже занят")

    teacher = User(
        full_name=full_name,
        login=login,
        role="teacher",
        email=data.get("email"),
        department=data.get("department"),
        position=data.get("position"),
        degree=data.get("degree"),
        contact=data.get("contact"),
    )
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher.to_dict()


@router.put("/{teacher_id}")
def update_teacher(teacher_id: int, data: dict, db: Session = Depends(get_db)):
    teacher = User.get_teacher(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")

    if "login" in data and data["login"] != teacher.login:
        existing = db.query(User).filter(User.login == data["login"]).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Логин '{data['login']}' уже занят")

    updatable = ["full_name", "login", "email", "department", "position", "degree", "contact"]
    for field in updatable:
        if field in data:
            setattr(teacher, field, data[field])

    db.commit()
    db.refresh(teacher)
    return teacher.to_dict()


@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = User.get_teacher(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")
    db.delete(teacher)
    db.commit()
    return {"status": "deleted"}