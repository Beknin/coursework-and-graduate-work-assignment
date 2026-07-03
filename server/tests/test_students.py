# tests/test_students.py
import pytest


def test_get_students(client, db, test_data):
    """Тест: получение всех студентов"""
    response = client.get("/api/students")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4


def test_create_student(client, db):
    """Тест: создание студента"""
    response = client.post("/api/students", json={
        "full_name": "Новый Студент",
        "course": 1,
        "group_name": "14125"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Новый Студент"


def test_create_student_invalid_course(client, db):
    """Тест: попытка создать студента с неверным курсом"""
    response = client.post("/api/students", json={
        "full_name": "Неверный Студент",
        "course": 5,
        "group_name": "14125"
    })
    assert response.status_code == 400
    assert "курс" in response.json()["detail"].lower()


def test_update_student(client, db, test_data):
    """Тест: обновление студента"""
    student = test_data["students"][0]
    response = client.put(f"/api/students/{student.id}", json={
        "full_name": "Обновлённый Студент",
        "course": 2,
        "group_name": "14126"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "updated"


def test_delete_student(client, db):
    """Тест: удаление студента"""
    response = client.post("/api/students", json={
        "full_name": "Студент на удаление",
        "course": 3,
        "group_name": "14123"
    })
    student_id = response.json()["id"]

    response = client.delete(f"/api/students/{student_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"
