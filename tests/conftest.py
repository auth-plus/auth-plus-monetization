from typing import Generator
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.config.database import engine
from src.presentation.server import app as FastApiApp


@pytest.fixture()
def app() -> Generator[FastAPI, None, None]:
    yield FastApiApp


@pytest.fixture()
def client(app) -> Generator[TestClient, None, None]:
    client = TestClient(app)
    yield client


@pytest.fixture()
def session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
