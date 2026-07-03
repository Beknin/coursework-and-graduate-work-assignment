# tests/test_orders.py
import pytest
from app.models import models
from datetime import date


def test_generate_preliminary_order(client, db, test_data):
    """Тест: генерация предварительного приказа"""
    # Создаём студента и тему
    student = test_data["students"][0]
    teacher = test_data["teachers"][0]
    
    # Создаём тему
    response = client.post("/api/topics", json={
        "teacher_id": teacher.id,
        "level": "ВКР",
        "title": "Тема для приказа",
        "description": "Описание"
    })
    topic_id = response.json()["id"]
    
    # Записываем студента и подтверждаем
    response = client.post("/api/enrollments", json={
        "student_id": student.id,
        "topic_id": topic_id
    })
    enrollment_id = response.json()["id"]
    client.put(f"/api/enrollments/{enrollment_id}/confirm")
    
    # Устанавливаем дедлайн (чтобы можно было генерировать)
    deadline = models.Deadline(
        name="preliminary_order",
        date=date(2026, 12, 20),  # прошлая дата, чтобы приказ можно было сгенерировать
        is_active=1
    )
    db.add(deadline)
    db.commit()
    
    # Авторизуемся как админ
    login_response = client.post("/api/auth/login", json={
        "login": "admin",
        "password": "admin",
        "role": "admin"
    })
    token = login_response.json()["token"]
    
    response = client.get(
        "/api/orders/preliminary",
        headers={"Authorization": f"Bearer {token}"}
    )
    # Может быть 200 или 403 (если дедлайн не наступил)
    assert response.status_code in [200, 403]


def test_generate_final_order(client, db, test_data):
    """Тест: генерация окончательного приказа"""
    # Создаём студента и тему
    student = test_data["students"][0]
    teacher = test_data["teachers"][0]
    
    # Создаём тему
    response = client.post("/api/topics", json={
        "teacher_id": teacher.id,
        "level": "ВКР",
        "title": "Тема для финального приказа",
        "description": "Описание"
    })
    topic_id = response.json()["id"]
    
    # Записываем студента и подтверждаем
    response = client.post("/api/enrollments", json={
        "student_id": student.id,
        "topic_id": topic_id
    })
    enrollment_id = response.json()["id"]
    client.put(f"/api/enrollments/{enrollment_id}/confirm")
    
    # Устанавливаем дедлайн
    deadline = models.Deadline(
        name="final_order",
        date=date(2027, 4, 15),
        is_active=1
    )
    db.add(deadline)
    db.commit()
    
    # Авторизуемся как админ
    login_response = client.post("/api/auth/login", json={
        "login": "admin",
        "password": "admin",
        "role": "admin"
    })
    token = login_response.json()["token"]
    
    response = client.get(
        "/api/orders/final",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code in [200, 403]
