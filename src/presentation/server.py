from uuid import UUID
from fastapi import FastAPI
from pydantic import BaseModel
from src.core import Core
from src.core.entity.account import AccountType
from src.config.database import engine

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
