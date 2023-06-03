from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient
from src.presentation.server import app as FastApiApp


@pytest.fixture()
def app() -> FastAPI:
    yield FastApiApp


@pytest.fixture()
def client(app) -> TestClient:
    client = TestClient(app)
    yield client
