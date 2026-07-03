# tests/test_teachers.py
import pytest


def test_get_teachers(client, db, test_data):
    """Тест: получение всех преподавателей"""
    response = client.get("/api/teachers")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4


def test_create_teacher(client, db):
    """Тест: создание преподавателя"""
    response = client.post("/api/teachers", json={
        "full_name": "Новый Преподаватель",
        "position": "Доцент",
        "degree": "к.т.н.",
        "contact": "new@email.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Новый Преподаватель"


def test_update_teacher(client, db, test_data):
    """Тест: обновление преподавателя"""
    teacher = test_data["teachers"][0]
    response = client.put(f"/api/teachers/{teacher.id}", json={
        "full_name": "Обновлённый Преподаватель",
        "position": "Профессор",
        "degree": "д.т.н.",
        "contact": "updated@email.com"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "updated"


def test_delete_teacher(client, db):
    """Тест: удаление преподавателя"""
    response = client.post("/api/teachers", json={
        "full_name": "Преподаватель на удаление",
        "position": "Доцент"
    })
    teacher_id = response.json()["id"]

    response = client.delete(f"/api/teachers/{teacher_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"
