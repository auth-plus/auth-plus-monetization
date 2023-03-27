FROM python:3.10.6-alpine AS dependency
WORKDIR /app

COPY . .
ENV POETRY_VERSION=1.4.1
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry install
# RUN poetry run flask --app auth-plus-monetization/presentation/server run
