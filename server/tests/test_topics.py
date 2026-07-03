import pytest


def test_get_topics(client, db, test_data):
    """Тест: получение всех тем"""
    response = client.get("/api/topics")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_topic(client, db, test_data):
    """Тест: создание темы"""
    teacher = test_data["teachers"][0]
    response = client.post("/api/topics", json={
        "teacher_id": teacher.id,
        "level": "Курсовая",
        "title": "Тестовая тема из Excel",
        "description": "Описание темы из тестов"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Тестовая тема из Excel"


def test_create_topic_without_teacher(client, db):
    """Тест: попытка создать тему без преподавателя"""
    response = client.post("/api/topics", json={
        "teacher_id": 999,
        "level": "ВКР",
        "title": "Тема без преподавателя"
    })
    assert response.status_code == 404


def test_get_free_topics(client, db, test_data):
    """Тест: получение свободных тем"""
    # Создаём тему
    teacher = test_data["teachers"][0]
    client.post("/api/topics", json={
        "teacher_id": teacher.id,
        "level": "Курсовая",
        "title": "Свободная тема",
        "description": "Описание"
    })
    
    response = client.get("/api/topics/free")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Проверяем, что статус free
    if data:
        assert data[0]["status"] == "free"


def test_delete_topic(client, db, test_data):
    """Тест: удаление темы"""
    # Создаём тему
    teacher = test_data["teachers"][0]
    response = client.post("/api/topics", json={
        "teacher_id": teacher.id,
        "level": "Курсовая",
        "title": "Тема для удаления"
    })
    topic_id = response.json()["id"]
    
    response = client.delete(f"/api/topics/{topic_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"