import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.config.database import engine
from src.presentation.server import app as FastApiApp


@pytest.fixture()
def app() -> FastAPI:
    yield FastApiApp


@pytest.fixture()
def client(app) -> TestClient:
    client = TestClient(app)
    yield client


@pytest.fixture()
def session() -> TestClient:
    with Session(engine) as session:
        yield session
