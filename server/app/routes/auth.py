from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Модель для входа
class LoginData(BaseModel):
    login: str
    password: str
    role: str  # admin, teacher, student

# Модель для ответа
class LoginResponse(BaseModel):
    token: str
    user: dict


@router.post("/login", response_model=LoginResponse)
def login(data: LoginData):
    """
    Вход в систему.
    В реальном проекте здесь будет проверка логина/пароля в БД.
    """
    # Пока просто заглушка для теста
    # В реальном проекте проверяйте данные в БД
    
    # Если логин и пароль не пустые — пропускаем
    if not data.login or not data.password:
        raise HTTPException(status_code=400, detail="Логин и пароль обязательны")
    
    # Создаём тестового пользователя
    user = {
        "id": 1,
        "full_name": data.login,
        "role": data.role
    }
    
    # Возвращаем токен и данные пользователя
    return LoginResponse(
        token=f"fake-jwt-token-for-{data.login}",
        user=user
    )


@router.post("/register")
def register(data: LoginData):
    """
    Регистрация нового пользователя.
    """
    # Здесь будет создание пользователя в БД
    return {"status": "registered", "login": data.login}