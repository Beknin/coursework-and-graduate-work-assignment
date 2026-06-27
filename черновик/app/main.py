import os
import sys
from pathlib import Path

# Добавляем корневую папку в путь, чтобы работали импорты
sys.path.append(str(Path(__file__).parent.parent))

from app.database.db import SessionLocal
from app.models.models import Base, Student, Teacher, Topic, Enrollment, Deadline
from app.controllers.topic_controller import TopicController
from app.controllers.enrollment_controller import EnrollmentController
from app.controllers.student_controller import StudentController
from app.controllers.teacher_controller import TeacherController
from app.controllers.deadline_controller import DeadlineController
from app.controllers.report_controller import ReportController
from app.utils.deadline_checker import DeadlineChecker
from app.utils.excel_parser import ExcelParser
from app.utils.word_generator import WordGenerator


def init_database():
    """Создаёт таблицы, если их нет"""
    from app.database.db import engine
    Base.metadata.create_all(bind=engine)
    print("✅ База данных инициализирована")


def get_controllers(db_session):
    """Возвращает все контроллеры с подключением к БД"""
    return {
        "topic": TopicController(db_session),
        "enrollment": EnrollmentController(db_session),
        "student": StudentController(db_session),
        "teacher": TeacherController(db_session),
        "deadline": DeadlineController(db_session),
        "report": ReportController(db_session),
    }


def main():
    """Главная функция — здесь будет запускаться Tkinter (напишет фронтендщик)"""
    # Инициализируем БД
    init_database()
    
    # Создаём сессию для работы с БД
    db_session = SessionLocal()
    
    # Получаем контроллеры
    controllers = get_controllers(db_session)
    
    # TODO: Здесь фронтендщик напишет код для запуска Tkinter
    # и передаст в него контроллеры
    
    print("✅ Приложение готово к работе")
    print("📋 Контроллеры:", list(controllers.keys()))
    
    # Пример использования (удалить потом):
    # topics = controllers["topic"].get_all_topics()
    # print(f"📚 Всего тем: {len(topics)}")


if __name__ == "__main__":
    main()