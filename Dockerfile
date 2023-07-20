FROM python:3.10.6-alpine
WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./
ENV POETRY_VERSION=1.4.1
RUN apk update
RUN apk add --no-cache --virtual build-deps gcc python3-dev musl-dev
RUN apk add postgresql-dev
RUN pip install --upgrade pip && pip install poetry==$POETRY_VERSION
RUN poetry config virtualenvs.create false && poetry install

COPY  . .

# For development
EXPOSE 8000

# For production/staging
EXPOSE 5004
EXPOSE 5566
