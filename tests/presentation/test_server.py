from copy import deepcopy
from datetime import datetime
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config.database import engine
from src.core.repository.account import account_table
from tests.factory.helpers import delete_account


def test_route_health(client: TestClient):
    response: Response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["server"] == "Ok"


def test_route_create_account(client: TestClient):
    # TESTING API
    external_id = uuid4()
    response: Response = client.post(
        "/account", json={"external_id": str(external_id), "type": "PRE_PAID"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["external_id"] == str(external_id)

    # TESTING DB
    with Session(engine) as session:
        select_query = (
            select(account_table).where(account_table.c.id == body["id"]).limit(1)
        )
        cursor = session.execute(select_query).first()
        if cursor is None:
            raise SystemError("test: test_route_create_account something went wrong")
        (id_, external_id, type_, created_at, deleted_at) = deepcopy(cursor)
        assert isinstance(id_, UUID)
        assert external_id == external_id
        assert type_.value == "PRE_PAID"
        assert isinstance(created_at, datetime)
        assert deleted_at is None
        delete_account(session, id_)
