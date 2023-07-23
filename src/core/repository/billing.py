from typing import List
from uuid import UUID

import requests

from src.config.envvar import EnvVars
from src.core.entity.billing import BillingUser, InvoiceItem
from src.core.tasks.create_charge import create_charge
from src.core.tasks.create_invoice import create_invoice
from src.core.usecase.driven.billing.billing_charge import BillingCharge
from src.core.usecase.driven.billing.billing_fetch_user import BillingFetchUser
from src.presentation.worker import huey


class BillingService(
    BillingFetchUser,
    BillingCharge,
):
    def fetch_by_account_id(self, external_id: UUID) -> BillingUser:
        resp = requests.get(f"{EnvVars.BILLING_HOST}/user/{external_id}")
        json = resp.json()
        return BillingUser(
            json["id"],
            json["external_id"],
        )

    def charge(self, external_id: UUID, item_list: List[InvoiceItem]):
        pipeline = create_invoice.s(external_id, item_list).then(create_charge)
        huey.enqueue(pipeline)
