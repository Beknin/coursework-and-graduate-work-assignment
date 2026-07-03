import pytest
import os
from app.services.order_service import OrderService


def test_generate_order():
    """Тест: генерация приказа в Word"""
    data = [
        {
            "student_name": "Бавлов Сергей Александрович",
            "group": "14121",
            "topic_title": "Разработка веб-приложения",
            "teacher_name": "Иванов Иван Иванович"
        },
        {
            "student_name": "Ганжитова Ирина Алдаровна",
            "group": "14124",
            "topic_title": "Создание нейросети",
            "teacher_name": "Петров Петр Петрович"
        }
    ]
    
    file_path = OrderService.generate_order(data, "test")
    assert os.path.exists(file_path)
    assert file_path.endswith(".docx")
    
    os.remove(file_path)


def test_generate_order_with_custom_path():
    """Тест: генерация приказа с указанным путём"""
    data = [
        {
            "student_name": "Тестов Студент",
            "group": "14121",
            "topic_title": "Тестовая тема",
            "teacher_name": "Тестов Преподаватель"
        }
    ]
    
    file_path = "custom_order.docx"
    result = OrderService.generate_order(data, "custom", file_path)
    assert os.path.exists(result)
    assert result == file_path
    
    os.remove(file_path)