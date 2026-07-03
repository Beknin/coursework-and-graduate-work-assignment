from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database.db import get_db
from app.models import models
from app.core.security import (
    hash_password, verify_password, create_access_token,
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()


# ===== СХЕМЫ =====
class LoginData(BaseModel):
    login: str
    password: str
    role: str  # admin, teacher, student


class RegisterData(BaseModel):
    full_name: str
    login: str
    password: str
    role: str  # admin, teacher, student


class TokenResponse(BaseModel):
    token: str
    token_type: str = "bearer"
    user: dict


# ===== ЭНДПОИНТЫ =====

@router.post("/login", response_model=TokenResponse)
def login(data: LoginData, db: Session = Depends(get_db)):
    """Вход в систему с проверкой в БД"""
    # 1. Ищем пользователя в БД
    user = db.query(models.User).filter(models.User.login == data.login).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )
    
    # 2. Проверяем роль
    if user.role != data.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Пользователь с ролью '{user.role}' не может войти как '{data.role}'"
        )
    
    # 3. Проверяем пароль
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )
    
    # 4. Создаём JWT-токен
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=None
    )
    
    # 5. Возвращаем результат
    return TokenResponse(
        token=access_token,
        user={
            "id": user.id,
            "full_name": user.full_name,
            "login": user.login,
            "role": user.role
        }
    )


@router.post("/register")
def register(data: RegisterData, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    # 1. Проверяем, не занят ли логин
    existing = db.query(models.User).filter(models.User.login == data.login).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Логин уже занят"
        )
    
    # 2. Хэшируем пароль
    hashed_password = hash_password(data.password)
    
    # 3. Создаём пользователя
    user = models.User(
        full_name=data.full_name,
        login=data.login,
        hashed_password=hashed_password,
        role=data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "status": "registered",
        "id": user.id,
        "login": user.login,
        "role": user.role
    }


@router.get("/me")
def get_me(current_user: models.User = Depends(get_current_user)):
    """Получить информацию о текущем пользователе"""
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "login": current_user.login,
        "role": current_user.role
    }