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
