from typing import List
from uuid import UUID

import requests
from celery import chain

from src.config.envvar import EnvVars
from src.config.worker import worker
from src.core.entity.billing import BillingUser, Charge, Invoice, InvoiceItem
from src.core.usecase.driven.billing.billing_charge import BillingCharge
from src.core.usecase.driven.billing.billing_fetch_user import BillingFetchUser


@worker.task()
def __create_invoice(external_id: UUID, item_list: list[InvoiceItem]) -> Invoice:
    resp = requests.post(
        f"{EnvVars.BILLING_HOST}/invoice",
        {"external_user_id": external_id, "itens": item_list},
    )
    json = resp.json()
    return Invoice(
        json.id,
        json.user_id,
        json.status,
        json.created_at,
    )


@worker.task()
def __create_charge(invoice_id: UUID) -> Charge:
    resp = requests.post(f"{EnvVars.BILLING_HOST}/charge", {"invoice_id": invoice_id})
    json = resp.json()
    return Charge(
        json.id,
        json.invoice_id,
        json.status,
        json.payment_method_id,
    )


class BillingService(
    BillingFetchUser,
    BillingCharge,
):
    def fetch_by_account_id(self, external_id: UUID) -> BillingUser:
        resp = requests.get(f"{EnvVars.BILLING_HOST}/user/{external_id}")
        json = resp.json()
        return BillingUser(
            json.id,
            json.external_id,
        )

    def charge(self, external_id: UUID, item_list: List[InvoiceItem]):
        chain(
            __create_invoice(external_id, item_list),
            __create_charge(),
        ).apply_async()
