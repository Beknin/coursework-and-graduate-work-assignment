import requests
from typing import Optional

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.token: Optional[str] = None

    def set_token(self, token: str):
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def clear_token(self):
        self.token = None
        self.session.headers.pop("Authorization", None)

    def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        
        print(f"🔍 Запрос: {method} {url}")
        if self.token:
            print(f"🔑 Токен: Bearer {self.token[:20]}...")
            if "headers" not in kwargs:
                kwargs["headers"] = {}
            kwargs["headers"]["Authorization"] = f"Bearer {self.token}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            print(f"✅ Статус: {response.status_code}")
            print(f"📄 Ответ: {response.text[:200]}")  # ← показываем первые 200 символов
            
            response.raise_for_status()
            
            # 🔥 Если ответ пустой — возвращаем None, а не падаем
            if not response.text or not response.text.strip():
                print("⚠️ Пустой ответ от сервера")
                return None
            
            return response.json()
            
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Не удалось подключиться к серверу")
        except requests.exceptions.HTTPError as e:
            # Пытаемся получить детали ошибки
            try:
                error_msg = response.json().get("detail", str(e))
            except:
                error_msg = response.text or str(e)
            print(f"❌ Ошибка: {error_msg}")
            raise Exception(error_msg)
        except ValueError as e:
            # 🔥 Ошибка парсинга JSON
            print(f"❌ Ошибка парсинга JSON: {e}")
            print(f"📄 Ответ: {response.text[:200]}")
            raise Exception(f"Сервер вернул не JSON: {response.text[:100]}")