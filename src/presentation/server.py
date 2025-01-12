from datetime import datetime
from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel

from src.core import Core

app = FastAPI()


@app.get("/health")
def health():
    return {"server": "Ok"}


class CreateAccountInput(BaseModel):
    external_id: UUID


@app.post("/account")
def create_account(body: CreateAccountInput):
    core = Core()
    account = core.account_create.create(body.external_id)
    return account


class ChargeDebitInput(BaseModel):
    external_id: UUID
    date_start: datetime


@app.post("/charge")
def charge_debit(body: ChargeDebitInput):
    core = Core()
    core.charge_debit.charge_debit()
    return "Ok"


@app.get("/ledger/{external_id}")
def get_total_credit(external_id: UUID):
    core = Core()
    amount = core.get_total_credit.get_total_credit(external_id)
    return amount


class ReceiveCreditInput(BaseModel):
    external_id: UUID
    amount: float


@app.post("/ledger/credit")
def receive_credit(body: ReceiveCreditInput):
    core = Core()
    charge = core.receive_credit.receive_credit(body.external_id, body.amount)
    return charge


class ReceiveEventInput(BaseModel):
    external_id: UUID
    event: str


@app.post("/ledger/debit")
def receive_event(body: ReceiveEventInput):
    core = Core()
    transaction = core.receive_event.receive_event(body.external_id, body.event)
    return transaction


class TransformToPostPaidInput(BaseModel):
    external_id: UUID


@app.patch("/account/to_post_paid")
def transform_to_post_paid(body: TransformToPostPaidInput):
    core = Core()
    core.transform_to_post_paid.transform_to_post_paid(body.external_id)


class TransformToPrePaidInput(BaseModel):
    external_id: UUID


@app.patch("/account/to_pre_paid")
def transform_to_pre_paid(body: TransformToPrePaidInput):
    core = Core()
    core.transform_to_pre_paid.transform_to_pre_paid(body.external_id)
