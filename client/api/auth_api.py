from .client import APIClient

class AuthAPI:
    def __init__(self, client: APIClient):
        self.client = client

    def login(self, login: str, password: str, role: str) -> dict:
        data = {"login": login, "password": password, "role": role}
        return self.client._request("POST", "/auth/login", json=data)

    def get_me(self) -> dict:
        return self.client._request("GET", "/auth/me")