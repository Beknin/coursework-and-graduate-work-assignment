# tests/test_enrollments.py
import pytest
from app.models import models


def test_enroll_student(client, db, test_data):
    """Тест: запись студента на тему"""
    student = test_data["students"][0]
    teacher = test_data["teachers"][0]
    
    # Создаём тему
    response = client.post("/api/topics", json={
        "teacher_id": teacher.id,
        "level": "Курсовая",
        "title": "Тема для записи",
        "description": "Описание"
    })
    topic_id = response.json()["id"]
    
    response = client.post("/api/enrollments", json={
        "student_id": student.id,
        "topic_id": topic_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"


def test_enroll_student_taken_topic(client, db, test_data):
    """Тест: попытка записаться на занятую тему"""
    student = test_data["students"][0]
    teacher = test_data["teachers"][0]
    
    # Создаём тему
    response = client.post("/api/topics", json={
        "teacher_id": teacher.id,
        "level": "Курсовая",
        "title": "Занятая тема"
    })
    topic_id = response.json()["id"]
    
    # Занимаем тему
    client.post("/api/enrollments", json={
        "student_id": student.id,
        "topic_id": topic_id
    })
    
    # Пытаемся записаться ещё раз
    response = client.post("/api/enrollments", json={
        "student_id": student.id,
        "topic_id": topic_id
    })
    assert response.status_code == 400
    assert "уже" in response.json()["detail"].lower()


def test_confirm_enrollment(client, db, test_data):
    """Тест: подтверждение записи преподавателем"""
    student = test_data["students"][0]
    teacher = test_data["teachers"][0]
    
    # Создаём тему
    response = client.post("/api/topics", json={
        "teacher_id": teacher.id,
        "level": "Курсовая",
        "title": "Тема для подтверждения"
    })
    topic_id = response.json()["id"]
    
    # Запись
    response = client.post("/api/enrollments", json={
        "student_id": student.id,
        "topic_id": topic_id
    })
    enrollment_id = response.json()["id"]
    
    # Подтверждение
    response = client.put(f"/api/enrollments/{enrollment_id}/confirm")
    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"


def test_reject_enrollment(client, db, test_data):
    """Тест: отклонение записи преподавателем"""
    student = test_data["students"][0]
    teacher = test_data["teachers"][0]
    
    # Создаём тему
    response = client.post("/api/topics", json={
        "teacher_id": teacher.id,
        "level": "Курсовая",
        "title": "Тема для отклонения"
    })
    topic_id = response.json()["id"]
    
    # Запись
    response = client.post("/api/enrollments", json={
        "student_id": student.id,
        "topic_id": topic_id
    })
    enrollment_id = response.json()["id"]
    
    # Отклонение
    response = client.put(f"/api/enrollments/{enrollment_id}/reject")
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"
