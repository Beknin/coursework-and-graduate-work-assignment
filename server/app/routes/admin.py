from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()


# ===== НОВЫЕ РОУТЫ ДЛЯ /users (без префикса) =====

@router.get("/users", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Получить всех пользователей"""
    users = db.query(models.User).all()
    return users


@router.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Создать нового пользователя"""
    db_user = models.User(
        full_name=user.full_name,
        role=user.role,
        login=user.full_name.lower().replace(" ", "_")  # генерируем логин автоматически
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Обновить пользователя"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    db_user.full_name = user.full_name
    db_user.role = user.role
    db_user.login = user.login
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Удалить пользователя"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    db.delete(db_user)
    db.commit()
    return {"status": "deleted"}


# ===== СТАРЫЕ РОУТЫ ДЛЯ /admin/users (для админа) =====

@router.get("/admin/users", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Получить всех пользователей (только админ)"""
    users = db.query(models.User).all()
    return users


@router.delete("/admin/users/{user_id}")
def delete_user_admin(user_id: int, db: Session = Depends(get_db)):
    """Удалить пользователя (только админ)"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    db.delete(user)
    db.commit()
    return {"status": "deleted"}


@router.put("/admin/users/{user_id}/role")
def change_user_role(user_id: int, new_role: str, db: Session = Depends(get_db)):
    """Сменить роль пользователя"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if new_role not in ["admin", "teacher", "student"]:
        raise HTTPException(status_code=400, detail="Недопустимая роль")
    
    user.role = new_role
    db.commit()
    db.refresh(user)
    
    return {"status": "updated", "id": user_id, "role": user.role}