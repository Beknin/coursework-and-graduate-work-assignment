from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import User

router = APIRouter()


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    """Получить всех пользователей."""
    users = db.query(User).all()
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "full_name": u.full_name,
            "login": u.login or "",
            "role": u.role,
            "email": u.email,
            "course": u.course,
            "group_name": u.group_name,
            "department": u.department,
            "position": u.position,
            "degree": u.degree,
            "contact": u.contact,
            "access_level": u.access_level,
        })
    return result


@router.get("/admin/users")
def get_all_users(db: Session = Depends(get_db)):
    """Получить всех пользователей (админ)."""
    return get_users(db)


@router.post("/users")
def create_user(user_data: dict, db: Session = Depends(get_db)):
    """Создать нового пользователя."""
    full_name = user_data.get("full_name")
    role = user_data.get("role", "student")
    login = user_data.get("login") or full_name.lower().replace(" ", "_")

    db_user = User(
        full_name=full_name,
        login=login,
        role=role,
        email=user_data.get("email"),
        course=user_data.get("course"),
        group_name=user_data.get("group_name"),
        department=user_data.get("department"),
        position=user_data.get("position"),
        degree=user_data.get("degree"),
        contact=user_data.get("contact"),
        access_level=user_data.get("access_level", "full" if role == "admin" else None),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "id": db_user.id,
        "full_name": db_user.full_name,
        "login": db_user.login,
        "role": db_user.role,
    }


@router.put("/users/{user_id}")
def update_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    """Обновить пользователя."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Обновляем только переданные поля
    updatable_fields = [
        "full_name", "login", "role", "email",
        "course", "group_name", "department",
        "position", "degree", "contact", "access_level"
    ]
    for field in updatable_fields:
        if field in user_data:
            setattr(user, field, user_data[field])

    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "full_name": user.full_name,
        "login": user.login,
        "role": user.role,
    }


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Удалить пользователя."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(user)
    db.commit()
    return {"status": "deleted"}


@router.delete("/admin/users/{user_id}")
def delete_user_admin(user_id: int, db: Session = Depends(get_db)):
    """Удалить пользователя (админ)."""
    return delete_user(user_id, db)


@router.put("/admin/users/{user_id}/role")
def change_user_role(user_id: int, new_role: str, db: Session = Depends(get_db)):
    """Сменить роль пользователя."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if new_role not in ["admin", "teacher", "student"]:
        raise HTTPException(status_code=400, detail="Недопустимая роль")

    user.role = new_role
    db.commit()

    return {"status": "updated", "id": user_id, "role": user.role}