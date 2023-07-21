import requests
from requests import HTTPError, JSONDecodeError, RequestException

from src.config.envvar import EnvVars
from src.config.logger import console
from src.core.entity.billing import Charge, Invoice
from src.core.tasks.helpers import is_valid_uuid
from src.presentation.worker import huey


@huey.task()
def create_charge(invoice: Invoice) -> Charge:
    return _create_charge(invoice)


def _create_charge(invoice: Invoice) -> Charge:
    try:
        resp = requests.post(
            f"{EnvVars.BILLING_HOST}/charge", {"invoice_id": invoice.id}
        )
        json = resp.json()
        return Charge(
            is_valid_uuid(json["id"]),
            is_valid_uuid(json["invoice_id"]),
            json["status"],
            is_valid_uuid(json["payment_method_id"]),
        )
    except HTTPError as exc:
        console.error(exc)
        raise exc
    except JSONDecodeError as exc:
        console.error(exc)
        raise exc
    except RequestException as exc:
        console.error(exc)
        raise exc
