from .client import APIClient


class EnrollmentsAPI:
    def __init__(self, client: APIClient):
        self.client = client

    def get_enrollments(self) -> list[dict]:
        return self.client._request("GET", "/api/enrollments/")

    def create_enrollment(self, student_id: int, topic_id: int) -> dict:
        return self.client._request("POST", "/api/enrollments/", json={
            "student_id": student_id,
            "topic_id": topic_id,
        })

    def confirm_enrollment(self, enrollment_id: int) -> dict:
        return self.client._request("PUT", f"/api/enrollments/{enrollment_id}/confirm")

    def reject_enrollment(self, enrollment_id: int, comment: str = None) -> dict:
        return self.client._request("PUT", f"/api/enrollments/{enrollment_id}/reject", json={
            "comment": comment
        })

    def delete_enrollment(self, enrollment_id: int):
        return self.client._request("DELETE", f"/api/enrollments/{enrollment_id}")