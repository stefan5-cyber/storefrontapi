FROM python:3.8-slim-bullseye

WORKDIR /backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

# install dependencies
RUN pip install --upgrade pip && pip install pipenv
COPY Pipfile Pipfile.lock /backend/
RUN pipenv install --system

COPY . .

EXPOSE 8000