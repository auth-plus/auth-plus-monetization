from datetime import datetime
from uuid import UUID

import requests
from requests import HTTPError, JSONDecodeError, RequestException

from src.config.envvar import EnvVars
from src.config.logger import console
from src.core.entity.billing import Invoice, InvoiceItem
from src.core.tasks.helpers import is_valid_uuid
from src.presentation.worker import huey


@huey.task(retries=2, retry_delay=10)
def create_invoice(external_id: UUID, item_list: list[InvoiceItem]) -> Invoice:
    return _create_invoice(external_id, item_list)


def _create_invoice(external_id: UUID, item_list: list[InvoiceItem]) -> Invoice:
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
            datetime.strptime(json["created_at"], "%d/%m/%y"),
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
