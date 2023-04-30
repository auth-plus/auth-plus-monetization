from uuid import UUID
import requests

from src.core.entity.billing import BillingUser, Charge, Invoice, InvoiceItem
from src.core.usecase.driven.creating_charge import CreatingCharge
from src.core.usecase.driven.creating_invoice import CreatingInvoice
from src.core.usecase.driven.fetch_billing_user import FetchBillingUser


class Billing(CreatingCharge, CreatingInvoice, FetchBillingUser):
    __billing_endpoint = "localhost:5002"

    def fetch_by_account_id(self, account_id: UUID) -> BillingUser:
        resp = requests.get(f"{self.__billing_endpoint}/user/{account_id}")
        json = resp.json()
        return BillingUser(
            json.id,
            json.external_id,
        )

    def create_invoice(self, account_id: UUID, item_list: list[InvoiceItem]) -> Invoice:
        resp = requests.post(
            f"{self.__billing_endpoint}/invoice",
            {"external_user_id": account_id, "itens": item_list},
        )
        json = resp.json()
        return Invoice(
            json.id,
            json.user_id,
            json.status,
            json.created_at,
        )

    def create_charge(self, invoice_id: UUID) -> Charge:
        resp = requests.post(
            f"{self.__billing_endpoint}/charge", {"invoice_id": invoice_id}
        )
        json = resp.json()
        return Charge(
            json.id,
            json.invoice_id,
            json.status,
            json.payment_method_id,
        )
