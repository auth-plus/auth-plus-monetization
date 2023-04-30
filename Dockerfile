FROM python:3.10.6-alpine AS dependency
WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./
ENV POETRY_VERSION=1.4.1
RUN pip install --upgrade pip && pip install poetry==$POETRY_VERSION
RUN poetry config virtualenvs.create false && poetry install

COPY  . .
EXPOSE 5004
EXPOSE 5566
