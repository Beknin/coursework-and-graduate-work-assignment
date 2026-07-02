# client/api/users_api.py
from api.client import APIClient

class UsersAPI:
    def __init__(self, client: APIClient):
        self.client = client

    def get_all_users(self) -> list[dict]:
        return self.client._request("GET", "/admin/users")

    def create_user(self, data: dict) -> dict:
        return self.client._request("POST", "/users", json=data)

    def update_user(self, user_id: int, data: dict) -> dict:
        return self.client._request("PUT", f"/users/{user_id}", json=data)

    def delete_user(self, user_id: int):
        return self.client._request("DELETE", f"/admin/users/{user_id}")

    def change_role(self, user_id: int, new_role: str) -> dict:
        return self.client._request(
            "PUT", f"/admin/users/{user_id}/role",
            json={"role": new_role}
        )


class StudentsAPI:
    def __init__(self, client: APIClient):
        self.client = client

    def get_students(self) -> list[dict]:
        return self.client._request("GET", "/api/students/")

    def create_student(self, data: dict) -> dict:
        return self.client._request("POST", "/api/students/", json=data)

    def update_student(self, student_id: int, data: dict) -> dict:
        return self.client._request("PUT", f"/api/students/{student_id}", json=data)

    def delete_student(self, student_id: int):
        return self.client._request("DELETE", f"/api/students/{student_id}")


class TeachersAPI:
    def __init__(self, client: APIClient):
        self.client = client

    def get_teachers(self) -> list[dict]:
        return self.client._request("GET", "/api/teachers/")

    def create_teacher(self, data: dict) -> dict:
        return self.client._request("POST", "/api/teachers/", json=data)

    def update_teacher(self, teacher_id: int, data: dict) -> dict:
        return self.client._request("PUT", f"/api/teachers/{teacher_id}", json=data)

    def delete_teacher(self, teacher_id: int):
        return self.client._request("DELETE", f"/api/teachers/{teacher_id}")