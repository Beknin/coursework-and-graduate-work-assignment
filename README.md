# 🎓 Система распределения тем курсовых и дипломных работ

Клиент-серверное приложение для автоматизации распределения тем ВКР и курсовых работ между студентами и преподавателями.

---

## 🚀 Быстрый старт

### 1. Клонировать репозиторий
```bash
git clone https://github.com/Beknin/coursework-and-graduate-work-assignment.git
cd coursework-and-graduate-work-assignment/server
```
### 2.Установить зависимости
```bash
poetry install
```

### 3. Запустить сервер
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Открыть в браузере
```bash
http://localhost:8000/docs
```

### 5.Запуск через Docker 
```bash
docker compose up --build
```

### 👥 Роли
Администратор — управление пользователями, темами, дедлайнами, приказами

Преподаватель — создание тем, подтверждение заявок

Студент — просмотр тем, запись, статус заявки


