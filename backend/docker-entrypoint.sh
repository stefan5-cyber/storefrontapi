#!/bin/bash

echo "Waiting for DB to start..."
./wait-for.sh db:5432
./wait-for.sh redis:6379

python /backend/manage.py makemigrations
python /backend/manage.py migrate

python /backend/manage.py seed_db

python /backend/manage.py createsuperuser --noinput

python /backend/manage.py runserver 0.0.0.0:8000 &
celery -A backend worker --loglevel=info

