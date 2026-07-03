FROM python:3.12-slim

WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry==2.4.1

# Копируем зависимости
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Копируем код
COPY . .

# Запускаем FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]