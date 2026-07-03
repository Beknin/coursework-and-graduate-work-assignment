# tests/test_auth.py
import pytest
from app.models import models
from app.core.security import hash_password


def test_login_success(client, db):
    """Тест: успешный вход"""
    user = models.User(
        full_name="Тест Пользователь",
        login="testuser",
        hashed_password=hash_password("password"),
        role="student"
    )
    db.add(user)
    db.commit()

    response = client.post("/api/auth/login", json={
        "login": "testuser",
        "password": "password",
        "role": "student"
    })
    assert response.status_code == 200
    assert "token" in response.json()


def test_login_invalid_role(client, db):
    """Тест: вход с неверной ролью"""
    user = models.User(
        full_name="Тест Пользователь",
        login="testuser2",
        hashed_password=hash_password("password"),
        role="student"
    )
    db.add(user)
    db.commit()

    response = client.post("/api/auth/login", json={
        "login": "testuser2",
        "password": "password",
        "role": "admin"
    })
    assert response.status_code in [403, 401]
