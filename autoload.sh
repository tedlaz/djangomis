#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata misall.json
python manage.py runserver 0.0.0.0:8000
