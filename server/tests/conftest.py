# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.db import Base, get_db
from app.models import models
from app.core.security import hash_password

# Тестовая БД
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db():
    """Фикстура для работы с тестовой БД"""
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def test_data(db):
    """Фикстура с тестовыми данными"""

    # Админ
    admin = models.User(
        full_name="Тестовый Админ",
        login="admin",
        hashed_password=hash_password("admin"),
        role="admin"
    )
    db.add(admin)

    # Студенты
    students_data = [
        {"full_name": "Бавлов Сергей Александрович", "course": 1, "group_name": "14121", "login": "bavlov"},
        {"full_name": "Ганжитова Ирина Алдаровна", "course": 1, "group_name": "14124", "login": "ganzhitova"},
        {"full_name": "Емельянова Татьяна Валерьевна", "course": 1, "group_name": "14122", "login": "emelyanova"},
        {"full_name": "Акмамедов Джумадурды", "course": 1, "group_name": "14123", "login": "akmamedov"},
    ]

    students = []
    for s_data in students_data:
        user = models.User(
            full_name=s_data["full_name"],
            login=s_data["login"],
            hashed_password=hash_password("password"),
            role="student"
        )
        db.add(user)
        db.flush()

        student = models.Student(
            id=user.id,
            course=s_data["course"],
            group_name=s_data["group_name"]
        )
        db.add(student)
        students.append(student)

    # Преподаватели
    teachers_data = [
        {"full_name": "Иванов Иван Иванович", "position": "Доцент", "degree": "к.т.н.", "contact": "ivanov@email.com"},
        {"full_name": "Петров Петр Петрович", "position": "Профессор", "degree": "д.ф.-м.н.", "contact": "petrov@email.com"},
    ]

    teachers = []
    for t_data in teachers_data:
        user = models.User(
            full_name=t_data["full_name"],
            login=t_data["full_name"].split()[0].lower(),
            hashed_password=hash_password("password"),
            role="teacher"
        )
        db.add(user)
        db.flush()

        teacher = models.Teacher(
            id=user.id,
            position=t_data["position"],
            degree=t_data["degree"],
            contact=t_data["contact"]
        )
        db.add(teacher)
        teachers.append(teacher)

    db.commit()

    return {
        "admin": admin,
        "students": students,
        "teachers": teachers
    }


@pytest.fixture(scope="function")
def auth_headers(client, db, test_data):
    """Фикстура для авторизации"""
    admin = test_data["admin"]
    response = client.post(
        "/api/auth/login",
        json={"login": "admin", "password": "admin", "role": "admin"}
    )
    token = response.json().get("token", "fake-token")
    return {"Authorization": f"Bearer {token}"}
