from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel

from src.core import Core
from src.core.entity.account import AccountType

app = FastAPI()


@app.get("/health")
def health():
    return {"server": "Ok"}


class CreateAccountInput(BaseModel):
    external_id: UUID
    type: AccountType


@app.post("/account")
def create_account(body: CreateAccountInput):
    core = Core()
    charge = core.account_create.create(body.external_id, body.type)
    return charge


class ReceiveEventInput(BaseModel):
    account_id: UUID
    event: str


@app.post("/event")
def receive_event(body: ReceiveEventInput):
    core = Core()
    charge = core.receive_event.receive_event(body.account_id, body.event)
    return charge
