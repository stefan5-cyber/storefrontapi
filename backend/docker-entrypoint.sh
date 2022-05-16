#!/bin/bash

echo "Waiting for DB to start..."
./wait-for.sh db:5432

python /backend/manage.py runserver 0.0.0.0:8000