# client/api/enrollments_api.py
from api.client import APIClient


class EnrollmentsAPI:
    def __init__(self, client: APIClient):
        self.client = client

    def enroll_student(self, student_id: int, topic_id: int) -> dict:
        data = {"student_id": student_id, "topic_id": topic_id}
        return self.client._request("POST", "/api/enrollments/", json=data)

    def confirm_enrollment(self, enrollment_id: int) -> dict:
        return self.client._request(
            "PUT", f"/api/enrollments/{enrollment_id}/confirm"
        )

    def reject_enrollment(self, enrollment_id: int) -> dict:
        return self.client._request(
            "PUT", f"/api/enrollments/{enrollment_id}/reject"
        )