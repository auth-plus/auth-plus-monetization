FROM python:3.12.3-slim AS dependency
WORKDIR /app

RUN apt update && apt install python3-dev libpq-dev gcc -y
RUN pip install pipx
RUN pipx install poetry==1.8.5
ENV PATH=/root/.local/bin:$PATH
RUN poetry --version
RUN poetry config virtualenvs.create false
COPY  . .
ENV VIRTUAL_ENV=/opt/env
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN poetry install --no-root

# For development
EXPOSE 8000

# For production/staging
EXPOSE 5004
