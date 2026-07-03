from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.models import models
from app.schemas import schemas
from app.core.security import get_current_admin, get_current_user

router = APIRouter()


# ===== ПОЛЬЗОВАТЕЛИ (только админ) =====

@router.get("/users", response_model=List[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)  # ← только админ
):
    """Получить всех пользователей"""
    users = db.query(models.User).all()
    return users


@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)  # ← только админ
):
    """Получить пользователя по ID"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.post("/users", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)  # ← только админ
):
    """Создать нового пользователя (админ)"""
    # Проверяем, не занят ли логин
    existing = db.query(models.User).filter(models.User.login == user.login).first()
    if existing:
        raise HTTPException(status_code=400, detail="Логин уже занят")
    
    # Создаём пользователя с паролем по умолчанию
    from app.core.security import hash_password
    db_user = models.User(
        full_name=user.full_name,
        login=user.login,
        hashed_password=hash_password("password"),  # пароль по умолчанию
        role=user.role
    )
    db.add(db_user)
    db.flush()
    
    # Создаём запись в соответствующей таблице
    if user.role == "student":
        student = models.Student(
            id=db_user.id,
            course=user.course or 1,
            group_name=user.group_name or ""
        )
        db.add(student)
    elif user.role == "teacher":
        teacher = models.Teacher(
            id=db_user.id,
            position=user.position or "",
            degree=user.degree or "",
            contact=user.contact or ""
        )
        db.add(teacher)
    elif user.role == "admin":
        admin = models.Admin(
            id=db_user.id,
            access_level="full"
        )
        db.add(admin)
    
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)  # ← только админ
):
    """Обновить данные пользователя"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Обновляем поля
    if user_data.full_name is not None:
        db_user.full_name = user_data.full_name
    if user_data.role is not None:
        db_user.role = user_data.role
    if user_data.password is not None:
        from app.core.security import hash_password
        db_user.hashed_password = hash_password(user_data.password)
    
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)  # ← только админ
):
    """Удалить пользователя"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Нельзя удалить самого себя
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Нельзя удалить самого себя")
    
    db.delete(user)
    db.commit()
    return {"status": "deleted", "id": user_id}


@router.put("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    new_role: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)  # ← только админ
):
    """Сменить роль пользователя"""
    if new_role not in ["admin", "teacher", "student"]:
        raise HTTPException(status_code=400, detail="Недопустимая роль")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Нельзя менять роль у самого себя
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Нельзя менять роль у самого себя")
    
    user.role = new_role
    db.commit()
    db.refresh(user)
    
    return {"status": "updated", "id": user_id, "role": user.role}


# ===== СТАТИСТИКА (только админ) =====

@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)  # ← только админ
):
    """Получить статистику по системе"""
    users_count = db.query(models.User).count()
    students_count = db.query(models.Student).count()
    teachers_count = db.query(models.Teacher).count()
    topics_count = db.query(models.Topic).count()
    enrollments_count = db.query(models.Enrollment).count()
    
    return {
        "total_users": users_count,
        "students": students_count,
        "teachers": teachers_count,
        "topics": topics_count,
        "enrollments": enrollments_count
    }