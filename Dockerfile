FROM python:3.11-slim

WORKDIR /app

# Копируем файлы зависимостей
COPY app/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY app/ ./app/
COPY static/ ./static/
COPY templates/ ./templates/
COPY *.json ./

# Создаем папку для данных
RUN mkdir -p /app/data

# Открываем порт
EXPOSE 5000

# Переменные окружения
ENV FLASK_APP=app/server.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Запускаем приложение
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
