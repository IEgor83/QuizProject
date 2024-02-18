# Используем базовый образ Python
FROM python:3.10

# Устанавливаем переменную среды PYTHONUNBUFFERED, чтобы обеспечить вывод логов в консоль без буферизации
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /code

# Копируем файл requirements.txt и устанавливаем зависимости
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /code/
