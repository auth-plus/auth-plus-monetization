from datetime import datetime
from uuid import UUID, uuid4

import responses

from src.config.envvar import EnvVars
from src.core.entity.billing import InvoiceItem
from src.core.tasks.create_invoice import _create_invoice


@responses.activate
def test_should_charge():
    external_id = uuid4()
    created_at = datetime.today()
    responses.add(
        responses.POST,
        f"{EnvVars.BILLING_HOST}/invoice",
        status=201,
        json={
            "id": str(uuid4()),
            "user_id": str(uuid4()),
            "status": "created",
            "created_at": created_at.strftime("%d/%m/%y"),
        },
    )
    invoice = _create_invoice(external_id, [InvoiceItem("descript", 1.0, "BRL", 1.0)])
    assert isinstance(invoice.id, UUID)
    assert isinstance(invoice.user_id, UUID)
    assert invoice.status == "created"
    assert isinstance(invoice.created_at, datetime)
    responses.assert_call_count(f"{EnvVars.BILLING_HOST}/invoice", 1)
