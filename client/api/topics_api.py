# client/api/topics_api.py
from api.client import APIClient


class TopicsAPI:
    def __init__(self, client: APIClient):
        self.client = client

    def get_topics(self) -> list[dict]:
        """Получить список всех тем"""
        return self.client._request("GET", "/api/topics")  # ← убрал слеш

    def get_free_topics(self) -> list[dict]:
        """Получить список свободных тем"""
        return self.client._request("GET", "/api/topics/free")

    def create_topic(self, data: dict) -> dict:
        """Создать новую тему"""
        return self.client._request("POST", "/api/topics", json=data)  # ← убрал слеш

    def update_topic(self, topic_id: int, data: dict) -> dict:
        """Обновить тему"""
        return self.client._request("PUT", f"/api/topics/{topic_id}", json=data)

    def delete_topic(self, topic_id: int):
        """Удалить тему"""
        return self.client._request("DELETE", f"/api/topics/{topic_id}")

    def get_topics_by_teacher(self, teacher_id: int) -> list[dict]:
        """Получить темы преподавателя"""
        return self.client._request("GET", f"/api/topics/teacher/{teacher_id}")