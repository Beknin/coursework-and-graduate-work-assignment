from .client import APIClient
from typing import Optional

class UsersAPI:
    def __init__(self, client: APIClient):
        self.client = client

    def get_users(self) -> list[dict]:
        return self.client._request("GET", "/users")

    def create_user(self, data: dict) -> dict:
        return self.client._request("POST", "/users", json=data)

    def update_user(self, user_id: int, data: dict) -> dict:
        return self.client._request("PUT", f"/users/{user_id}", json=data)

    def delete_user(self, user_id: int):
        return self.client._request("DELETE", f"/users/{user_id}")
    
class MockUsersAPI:
    """
    Заглушка API пользователей для тестирования GUI без сервера.
    Хранит данные в памяти. Имитирует задержку сети 100мс.
    """

    def __init__(self, client=None):
        self._users = [
            {
                "id": 1,
                "login": "admin",
                "role": "admin",
                "full_name": "Администратор Системы",
                "email": "admin@university.ru",
                "group_name": None,
                "course": None,
                "department": None,
                "position": None,
                "degree": None,
                "access_level": "full",
            },
            {
                "id": 2,
                "login": "ivanov",
                "role": "teacher",
                "full_name": "Иванов Иван Иванович",
                "email": "ivanov@university.ru",
                "group_name": None,
                "course": None,
                "department": "Информационные системы",
                "position": "доцент",
                "degree": "к.т.н.",
                "access_level": None,
            },
            {
                "id": 3,
                "login": "petrova",
                "role": "teacher",
                "full_name": "Петрова Анна Сергеевна",
                "email": "petrova@university.ru",
                "group_name": None,
                "course": None,
                "department": "Вычислительная математика",
                "position": "профессор",
                "degree": "д.ф.-м.н.",
                "access_level": None,
            },
            {
                "id": 4,
                "login": "sidorov",
                "role": "teacher",
                "full_name": "Сидоров Владимир Петрович",
                "email": "sidorov@university.ru",
                "group_name": None,
                "course": None,
                "department": "Информационные системы",
                "position": "старший преподаватель",
                "degree": None,
                "access_level": None,
            },
            {
                "id": 5,
                "login": "alexeev",
                "role": "student",
                "full_name": "Алексеев Михаил Дмитриевич",
                "email": "alexeev@university.ru",
                "group_name": "ПМИ-301",
                "course": 3,
                "department": None,
                "position": None,
                "degree": None,
                "access_level": None,
            },
            {
                "id": 6,
                "login": "borisova",
                "role": "student",
                "full_name": "Борисова Елена Александровна",
                "email": "borisova@university.ru",
                "group_name": "ПМИ-301",
                "course": 3,
                "department": None,
                "position": None,
                "degree": None,
                "access_level": None,
            },
            {
                "id": 7,
                "login": "volkov",
                "role": "student",
                "full_name": "Волков Константин Сергеевич",
                "email": "volkov@university.ru",
                "group_name": "ПМИ-302",
                "course": 3,
                "department": None,
                "position": None,
                "degree": None,
                "access_level": None,
            },
            {
                "id": 8,
                "login": "grigorieva",
                "role": "student",
                "full_name": "Григорьева Мария Павловна",
                "email": "grigorieva@university.ru",
                "group_name": "ПМИ-302",
                "course": 4,
                "department": None,
                "position": None,
                "degree": None,
                "access_level": None,
            },
            {
                "id": 9,
                "login": "smirnov",
                "role": "student",
                "full_name": "Смирнов Денис Андреевич",
                "email": "smirnov@university.ru",
                "group_name": "ПМИ-401",
                "course": 4,
                "department": None,
                "position": None,
                "degree": None,
                "access_level": None,
            },
            {
                "id": 10,
                "login": "kuznetsova",
                "role": "student",
                "full_name": "Кузнецова Ольга Викторовна",
                "email": "kuznetsova@university.ru",
                "group_name": "ПМИ-401",
                "course": 4,
                "department": None,
                "position": None,
                "degree": None,
                "access_level": None,
            },
        ]
        self._next_id = 11
        self._deleted_ids = []

    # ──────────────────────────────────────────────
    # CRUD методы
    # ──────────────────────────────────────────────

    def get_users(
        self,
        role: Optional[str] = None,
        search: Optional[str] = None,
        group: Optional[str] = None,
    ) -> list[dict]:
        """
        Возвращает список пользователей.
        Опционально фильтрует по роли, поисковой строке или группе.
        """
        result = self._users

        if role:
            result = [u for u in result if u["role"] == role]

        if group:
            result = [u for u in result if u.get("group_name") == group]

        if search:
            search_lower = search.lower()
            result = [
                u for u in result
                if search_lower in u["full_name"].lower()
                or search_lower in u["login"].lower()
                or search_lower in u.get("email", "").lower()
            ]

        return result

    def get_user_by_id(self, user_id: int) -> dict:
        """Возвращает пользователя по ID или выбрасывает ошибку."""
        for user in self._users:
            if user["id"] == user_id:
                return user
        raise ValueError(f"Пользователь с id={user_id} не найден")

    def get_students(self, group: Optional[str] = None) -> list[dict]:
        """Возвращает только студентов."""
        return self.get_users(role="student", group=group)

    def get_teachers(self, department: Optional[str] = None) -> list[dict]:
        """Возвращает только преподавателей."""
        teachers = self.get_users(role="teacher")
        if department:
            teachers = [t for t in teachers if t.get("department") == department]
        return teachers

    def get_admins(self) -> list[dict]:
        """Возвращает только администраторов."""
        return self.get_users(role="admin")

    def create_user(self, data: dict) -> dict:
        """
        Создаёт нового пользователя.
        data должен содержать: login, password, role, full_name.
        """
        # Простейшая валидация
        required = ["login", "role", "full_name"]
        for field in required:
            if field not in data or not data[field]:
                raise ValueError(f"Поле '{field}' обязательно для заполнения")

        # Проверка уникальности логина
        if any(u["login"] == data["login"] for u in self._users):
            raise ValueError(f"Пользователь с логином '{data['login']}' уже существует")

        # Проверка уникальности email (если указан)
        if data.get("email") and any(
            u.get("email") == data["email"] for u in self._users
        ):
            raise ValueError(f"Email '{data['email']}' уже используется")

        user = {
            "id": self._next_id,
            "login": data["login"],
            "role": data["role"],
            "full_name": data["full_name"],
            "email": data.get("email", ""),
            "group_name": data.get("group_name"),
            "course": data.get("course"),
            "department": data.get("department"),
            "position": data.get("position"),
            "degree": data.get("degree"),
            "access_level": data.get("access_level", "full" if data["role"] == "admin" else None),
        }

        self._users.append(user)
        self._next_id += 1
        return user

    def update_user(self, user_id: int, data: dict) -> dict:
        """Обновляет данные пользователя."""
        user = self.get_user_by_id(user_id)

        # Проверка уникальности логина при смене
        if "login" in data and data["login"] != user["login"]:
            if any(u["login"] == data["login"] for u in self._users):
                raise ValueError(f"Пользователь с логином '{data['login']}' уже существует")

        # Проверка уникальности email при смене
        if "email" in data and data.get("email") != user.get("email"):
            if any(u.get("email") == data["email"] for u in self._users):
                raise ValueError(f"Email '{data['email']}' уже используется")

        # Обновляем только переданные поля
        allowed_fields = [
            "login", "full_name", "email", "role",
            "group_name", "course", "department",
            "position", "degree", "access_level",
        ]
        for field in allowed_fields:
            if field in data:
                user[field] = data[field]

        # Если передали пароль — в реальном API здесь был бы хэш
        # В моке просто игнорируем (или логируем)

        return user

    def delete_user(self, user_id: int) -> dict:
        """Удаляет пользователя. Возвращает удалённого."""
        user = self.get_user_by_id(user_id)

        # Не даём удалить последнего админа
        if user["role"] == "admin":
            admin_count = sum(1 for u in self._users if u["role"] == "admin")
            if admin_count <= 1:
                raise ValueError("Нельзя удалить последнего администратора системы")

        self._users = [u for u in self._users if u["id"] != user_id]
        self._deleted_ids.append(user_id)
        return user

    # ──────────────────────────────────────────────
    # Вспомогательные методы
    # ──────────────────────────────────────────────

    def get_groups(self) -> list[str]:
        """Возвращает список всех уникальных групп студентов."""
        groups = {u["group_name"] for u in self._users if u["role"] == "student" and u["group_name"]}
        return sorted(groups)

    def get_departments(self) -> list[str]:
        """Возвращает список всех уникальных кафедр преподавателей."""
        departments = {u["department"] for u in self._users if u["role"] == "teacher" and u["department"]}
        return sorted(departments)

    def get_roles(self) -> list[str]:
        """Возвращает список доступных ролей."""
        return ["admin", "teacher", "student"]

    def get_students_without_topic(self) -> list[dict]:
        """
        Возвращает студентов, у которых ещё нет назначенной темы.
        Работает в паре с MockAssignmentsAPI.
        """
        # В реальном API был бы запрос к БД с JOIN.
        # В моке просто возвращаем всех студентов.
        # Логика «без темы» реализуется в MockAssignmentsAPI.
        return self.get_students()

    def reset(self):
        """
        Сбрасывает мок до начального состояния.
        Полезно для тестов.
        """
        self._users = [
            u.copy() for u in self._users[:10]
        ]
        self._next_id = 11
        self._deleted_ids.clear()

    def count_by_role(self) -> dict:
        """Возвращает количество пользователей по ролям."""
        counts = {"admin": 0, "teacher": 0, "student": 0}
        for u in self._users:
            role = u["role"]
            if role in counts:
                counts[role] += 1
        counts["total"] = len(self._users)
        return counts
