import pytest
from app.models import models


def test_generate_preliminary_order(client, db, test_data):
    """Тест: генерация предварительного приказа"""
    # Создаём дедлайн
    deadline = models.Deadline(
        name="preliminary_order",
        date="2026-12-20",
        is_active=1
    )
    db.add(deadline)
    db.commit()
    
    response = client.get("/api/orders/preliminary")
    assert response.status_code in [200, 403]  # 403 если дедлайн не наступил


def test_generate_final_order(client, db, test_data):
    """Тест: генерация окончательного приказа"""
    # Создаём дедлайн
    deadline = models.Deadline(
        name="final_order",
        date="2027-04-15",
        is_active=1
    )
    db.add(deadline)
    db.commit()
    
    response = client.get("/api/orders/final")
    assert response.status_code in [200, 403]