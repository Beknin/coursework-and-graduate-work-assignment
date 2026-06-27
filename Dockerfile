FROM python:3.12-slim

# Устанавливаем Tkinter и системные зависимости (X11)
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем только файлы с зависимостями (для кеширования слоёв)
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry и зависимости
RUN pip install poetry==2.4.1 \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Копируем весь код
COPY . .

# Точка входа (у вас будет основной файл приложения)
CMD ["python3", "app/main.py"]