# client/api/users_api.py
from api.client import APIClient


class UsersAPI:
    """API для работы с пользователями (админ)"""
    
    def __init__(self, client: APIClient):
        self.client = client

    def get_all_users(self) -> list[dict]:
        """Получить список всех пользователей (только админ)"""
        return self.client._request("GET", "/api/admin/users")

    def get_user(self, user_id: int) -> dict:
        """Получить пользователя по ID (только админ)"""
        return self.client._request("GET", f"/api/admin/users/{user_id}")

    def create_user(self, data: dict) -> dict:
        """Создать нового пользователя (только админ)"""
        return self.client._request("POST", "/api/admin/users", json=data)

    def update_user(self, user_id: int, data: dict) -> dict:
        """Обновить пользователя (только админ)"""
        return self.client._request("PUT", f"/api/admin/users/{user_id}", json=data)

    def delete_user(self, user_id: int):
        """Удалить пользователя (только админ)"""
        return self.client._request("DELETE", f"/api/admin/users/{user_id}")

    def change_role(self, user_id: int, new_role: str) -> dict:
        """Сменить роль пользователя (только админ)"""
        return self.client._request(
            "PUT", f"/api/admin/users/{user_id}/role",
            json={"role": new_role}
        )

    def get_stats(self) -> dict:
        """Получить статистику по системе (только админ)"""
        return self.client._request("GET", "/api/admin/stats")


class StudentsAPI:
    """API для работы со студентами"""
    
    def __init__(self, client: APIClient):
        self.client = client

    def get_students(self) -> list[dict]:
        """Получить список всех студентов"""
        return self.client._request("GET", "/api/students")

    def get_student(self, student_id: int) -> dict:
        """Получить студента по ID"""
        return self.client._request("GET", f"/api/students/{student_id}")

    def create_student(self, data: dict) -> dict:
        """Создать студента"""
        return self.client._request("POST", "/api/students", json=data)

    def update_student(self, student_id: int, data: dict) -> dict:
        """Обновить студента"""
        return self.client._request("PUT", f"/api/students/{student_id}", json=data)

    def delete_student(self, student_id: int):
        """Удалить студента"""
        return self.client._request("DELETE", f"/api/students/{student_id}")


class TeachersAPI:
    """API для работы с преподавателями"""
    
    def __init__(self, client: APIClient):
        self.client = client

    def get_teachers(self) -> list[dict]:
        """Получить список всех преподавателей"""
        return self.client._request("GET", "/api/teachers")

    def get_teacher(self, teacher_id: int) -> dict:
        """Получить преподавателя по ID"""
        return self.client._request("GET", f"/api/teachers/{teacher_id}")

    def create_teacher(self, data: dict) -> dict:
        """Создать преподавателя"""
        return self.client._request("POST", "/api/teachers", json=data)

    def update_teacher(self, teacher_id: int, data: dict) -> dict:
        """Обновить преподавателя"""
        return self.client._request("PUT", f"/api/teachers/{teacher_id}", json=data)

    def delete_teacher(self, teacher_id: int):
        """Удалить преподавателя"""
        return self.client._request("DELETE", f"/api/teachers/{teacher_id}")