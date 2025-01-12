import datetime
from typing import List
from uuid import UUID

import requests
from requests import HTTPError, JSONDecodeError, RequestException

from src.config.envvar import EnvVars
from src.config.logger import console
from src.core.entity.billing import BillingUser, Charge, Invoice, InvoiceItem
from src.core.helpers import is_valid_uuid
from src.core.usecase.driven.billing.billing_fetch_user import BillingFetchUser
from src.core.usecase.driven.billing.billing_fetching_invoice import (
    BillingFetchingInvoice,
    NoDraftInvoiceFound,
)
from src.core.usecase.driven.billing.billing_updating_invoice import (
    BillingUpdatingInvoice,
)


class BillingService(BillingFetchUser, BillingFetchingInvoice, BillingUpdatingInvoice):
    def fetch_by_account_id(self, external_id: UUID) -> BillingUser:
        resp = requests.get(f"{EnvVars.BILLING_HOST}/user/{external_id}")
        json = resp.json()
        return BillingUser(
            json["id"],
            json["external_id"],
        )

    def get_current(self, external_id: UUID) -> Invoice:
        resp = requests.get(
            f"{EnvVars.BILLING_HOST}/invoice/current?user_id={external_id}"
        )
        json = resp.json()
        if json["status"] != "draft":
            raise NoDraftInvoiceFound("No invoice on status draft was fetched")
        return Invoice(
            json["id"],
            external_id,
            json["status"],
            json["created_at"],
        )

    def add_item(self, external_id: UUID, item_list: List[InvoiceItem]) -> Invoice:
        try:
            resp = requests.post(
                f"{EnvVars.BILLING_HOST}/invoice",
                {"external_user_id": external_id, "itens": item_list},
            )
            json = resp.json()
            invoice = Invoice(
                is_valid_uuid(json["id"]),
                is_valid_uuid(json["user_id"]),
                json["status"],
                datetime.datetime.strptime(json["created_at"], "%Y-%m-%d"),
            )
            return invoice
        except HTTPError as exc:
            console.error(exc)
            raise exc
        except JSONDecodeError as exc:
            console.error(exc)
            raise exc
        except RequestException as exc:
            console.error(exc)
            raise exc

    def charge(self, invoice_id: UUID) -> Charge:
        try:
            resp = requests.post(
                f"{EnvVars.BILLING_HOST}/charge",
                {"invoice_id": invoice_id},
            )
            json = resp.json()
            invoice = Charge(
                is_valid_uuid(json["id"]),
                is_valid_uuid(json["invoice_id"]),
                json["status"],
                json["payment_method_id"],
            )
            return invoice
        except HTTPError as exc:
            console.error(exc)
            raise exc
        except JSONDecodeError as exc:
            console.error(exc)
            raise exc
        except RequestException as exc:
            console.error(exc)
            raise exc
