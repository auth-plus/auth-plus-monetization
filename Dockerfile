FROM python:3.12-alpine
WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./
RUN apk update
RUN apk add --no-cache --virtual build-deps gcc python3-dev musl-dev
RUN apk add postgresql-dev
RUN pip install --upgrade pip && pip install poetry==1.4.1
RUN poetry config virtualenvs.create false && poetry install

COPY  . .

# For development
EXPOSE 8000

# For production/staging
EXPOSE 5004
