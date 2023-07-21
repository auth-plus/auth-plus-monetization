from datetime import datetime
from uuid import UUID, uuid4

import responses

from src.config.envvar import EnvVars
from src.core.entity.billing import Invoice
from src.core.tasks.create_charge import _create_charge


@responses.activate
def test_should_charge():
    invoice = Invoice(
        uuid4(),
        uuid4(),
        "status",
        datetime.today(),
    )
    payment_method_id = uuid4()
    responses.add(
        responses.POST,
        f"{EnvVars.BILLING_HOST}/charge",
        status=201,
        json={
            "id": str(uuid4()),
            "invoice_id": str(invoice.id),
            "status": "created",
            "payment_method_id": str(payment_method_id),
        },
    )
    charge = _create_charge(invoice)
    assert isinstance(charge.id, UUID)
    assert charge.invoice_id == invoice.id
    assert charge.status == "created"
    assert charge.payment_method_id == payment_method_id
    responses.assert_call_count(f"{EnvVars.BILLING_HOST}/charge", 1)
