# Використання базового образу Python
FROM python:3.12-slim

# Встановлення робочої директорії в контейнері
WORKDIR /app

# Копіювання файлів додатку у контейнер
COPY . .

# Встановлення залежностей
RUN pip install --no-cache-dir -r requirements.txt

# Створення директорії для збереження даних
RUN mkdir -p storage

# Відкриття порту для додатку
EXPOSE 3000

# Команда для запуску додатку
CMD ["python", "main.py"]
