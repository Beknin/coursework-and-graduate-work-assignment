from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import User

router = APIRouter()


@router.get("/api/students/")
def get_students(db: Session = Depends(get_db)):
    students = db.query(User).filter(User.role == "student").all()
    result = []
    for s in students:
        result.append({
            "id": s.id,
            "full_name": s.full_name,
            "login": s.login,
            "role": "student",
            "email": s.email,
            "course": s.course,
            "group_name": s.group_name,
        })
    return result


@router.post("/api/students/")
def create_student(data: dict, db: Session = Depends(get_db)):
    """Создать студента."""
    full_name = data.get("full_name")
    student = User(
        full_name=full_name,
        login=data.get("login") or full_name.lower().replace(" ", "_"),
        role="student",
        email=data.get("email"),
        course=data.get("course", 1),
        group_name=data.get("group_name"),
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return {
        "id": student.id,
        "full_name": student.full_name,
        "role": "student",
    }


@router.put("/api/students/{student_id}")
def update_student(student_id: int, data: dict, db: Session = Depends(get_db)):
    student = db.query(User).filter(User.id == student_id, User.role == "student").first()
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")

    for field in ["full_name", "login", "email", "course", "group_name"]:
        if field in data:
            setattr(student, field, data[field])

    db.commit()
    return {"id": student.id, "full_name": student.full_name}


@router.delete("/api/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(User).filter(User.id == student_id, User.role == "student").first()
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    db.delete(student)
    db.commit()
    return {"status": "deleted"}