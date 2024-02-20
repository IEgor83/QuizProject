#!/bin/sh

python manage.py migrate

exec gunicorn QuizProject.wsgi:application -w 4 -b 0.0.0.0:8000