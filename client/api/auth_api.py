from api.client import APIClient

class AuthAPI:
    def __init__(self, client: APIClient):
        self.client = client

    def login(self, login: str, password: str, role: str) -> dict:
        data = {"login": login, "password": password, "role": role}
        return self.client._request("POST", "/auth/login", json=data)

    def register(self, login: str, password: str, role: str) -> dict:
        data = {"login": login, "password": password, "role": role}
        return self.client._request("POST", "/auth/register", json=data)
    
class MockAuthAPI:
    def login(self, login: str, password: str, role: str):
        return {
            "token": "fake-token-123",
            "user": {
                "id": 1,
                "login": login,
                "role": role,
                "full_name": "Тестовый Пользователь",
                "group": "ПМИ-301" if role == "student" else None,
                "department": "ИС" if role == "teacher" else None,
            }
        }

    def get_me(self):
        return self.login("admin", "pass", "admin")["user"]
