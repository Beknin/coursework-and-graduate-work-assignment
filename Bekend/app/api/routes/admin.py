from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()


def admin_required(user: models.User):
    """Проверка, что пользователь — администратор"""
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Только для администратора")


@router.get("/users", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Получить всех пользователей (только админ)"""
    users = db.query(models.User).all()
    return users


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Удалить пользователя (только админ)"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    db.delete(user)
    db.commit()
    return {"status": "deleted"}