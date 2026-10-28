FROM python:3.15.2-slim AS dependency
WORKDIR /app

RUN apt update && apt install python3-dev libpq-dev gcc -y
RUN pip install pipx
RUN pipx install uv==2.4.1
ENV PATH=/root/.local/bin:$PATH
RUN uv --version
RUN uv config virtualenvs.create false
COPY  . .
ENV VIRTUAL_ENV=/opt/env
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN uv install --no-root

# For development
EXPOSE 8000

# For production/staging
EXPOSE 5004
