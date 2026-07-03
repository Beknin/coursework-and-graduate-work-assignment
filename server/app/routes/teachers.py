from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import User

router = APIRouter()


@router.get("/api/teachers/")
def get_teachers(db: Session = Depends(get_db)):
    """Получить всех преподавателей."""
    teachers = db.query(User).filter(User.role == "teacher").all()
    result = []
    for t in teachers:
        result.append({
            "id": t.id,
            "full_name": t.full_name,
            "login": t.login,
            "role": "teacher",
            "email": t.email,
            "department": t.department,
            "position": t.position,
            "degree": t.degree,
            "contact": t.contact,
        })
    return result


@router.post("/api/teachers/")
def create_teacher(data: dict, db: Session = Depends(get_db)):
    """Создать преподавателя."""
    full_name = data.get("full_name")
    teacher = User(
        full_name=full_name,
        login=data.get("login") or full_name.lower().replace(" ", "_"),
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
    return {
        "id": teacher.id,
        "full_name": teacher.full_name,
        "role": "teacher",
    }


@router.put("/api/teachers/{teacher_id}")
def update_teacher(teacher_id: int, data: dict, db: Session = Depends(get_db)):
    teacher = db.query(User).filter(User.id == teacher_id, User.role == "teacher").first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")

    for field in ["full_name", "login", "email", "department", "position", "degree", "contact"]:
        if field in data:
            setattr(teacher, field, data[field])

    db.commit()
    return {"id": teacher.id, "full_name": teacher.full_name}


@router.delete("/api/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(User).filter(User.id == teacher_id, User.role == "teacher").first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")
    db.delete(teacher)
    db.commit()
    return {"status": "deleted"}