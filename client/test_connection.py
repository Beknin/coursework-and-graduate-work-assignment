"""Тест связи с сервером."""
from api.client import APIClient
import requests

client = APIClient("http://localhost:8000")

# 1. Health
print("1. Health:", end=" ")
try:
    print(client._request("GET", "/health"))
except Exception as e:
    print(f"ОШИБКА: {e}")

# 2. Логин
print("\n2. Логин:", end=" ")
try:
    result = client._request("POST", "/auth/login", json={
        "login": "admin", "password": "123", "role": "admin"
    })
    token = result.get("token", "")
    print(f"OK (token: {token[:20]}...)")
    client.set_token(token)
    print(f"   Полный ответ: {result}")
except Exception as e:
    print(f"ОШИБКА: {e}")

# 3. Список пользователей — с детальной отладкой
print("\n3. Пользователи (/admin/users):", end=" ")
try:
    # Попробуем напрямую через requests для деталей
    url = "http://localhost:8000/admin/users"
    headers = {"Authorization": f"Bearer {client.token}"}
    print(f"\n   URL: {url}")
    print(f"   Headers: {headers}")
    
    response = requests.get(url, headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Body (первые 200 символов): {response.text[:200]}")
    
    if response.status_code == 200:
        users = response.json()
        print(f"   OK ({len(users)} чел.)")
    else:
        print(f"   ОШИБКА: статус {response.status_code}")
except Exception as e:
    print(f"   ОШИБКА: {e}")

# 4. Попробуем /users (без /admin)
print("\n4. Пользователи (/users):", end=" ")
try:
    url = "http://localhost:8000/users"
    headers = {"Authorization": f"Bearer {client.token}"}
    response = requests.get(url, headers=headers)
    print(f"\n   URL: {url}")
    print(f"   Status: {response.status_code}")
    print(f"   Body (первые 200 символов): {response.text[:200]}")
    
    if response.status_code == 200:
        users = response.json()
        print(f"   OK ({len(users)} чел.)")
    else:
        print(f"   ОШИБКА: статус {response.status_code}")
except Exception as e:
    print(f"   ОШИБКА: {e}")

# 5. Студенты
print("\n5. Студенты (/api/students/):", end=" ")
try:
    url = "http://localhost:8000/api/students/"
    headers = {"Authorization": f"Bearer {client.token}"}
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}, Body: {response.text[:100]}")
except Exception as e:
    print(f"ОШИБКА: {e}")

# 6. Преподаватели
print("\n6. Преподаватели (/api/teachers/):", end=" ")
try:
    url = "http://localhost:8000/api/teachers/"
    headers = {"Authorization": f"Bearer {client.token}"}
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}, Body: {response.text[:100]}")
except Exception as e:
    print(f"ОШИБКА: {e}")

# 7. Темы
print("\n7. Темы:", end=" ")
try:
    topics = client._request("GET", "/api/topics/")
    print(f"OK ({len(topics)} тем)")
except Exception as e:
    print(f"ОШИБКА: {e}")