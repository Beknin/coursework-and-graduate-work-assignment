# client/api/topics_api.py
from .client import APIClient


class TopicsAPI:
    def __init__(self, client: APIClient):
        self.client = client

    def get_topics(self) -> list[dict]:
        return self.client._request("GET", "/api/topics/")

    def get_free_topics(self) -> list[dict]:
        return self.client._request("GET", "/api/topics/free")

    def create_topic(self, data: dict) -> dict:
        return self.client._request("POST", "/api/topics/", json=data)

    def update_topic(self, topic_id: int, data: dict) -> dict:
        return self.client._request("PUT", f"/api/topics/{topic_id}", json=data)

    def delete_topic(self, topic_id: int):
        return self.client._request("DELETE", f"/api/topics/{topic_id}")