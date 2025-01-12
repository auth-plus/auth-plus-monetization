import datetime
from uuid import uuid4

import responses
from sqlalchemy.orm import Session

from src.config.envvar import EnvVars
from src.core.entity.account import AccountType
from src.presentation.worker import post_paid_automation_charge
from tests.factory.helpers import (
    create_account,
    create_transaction,
    delete_account,
    delete_transaction,
    get_event,
)


@responses.activate
def test_worker_post_paid_automation_charge(session: Session):
    one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    account = create_account(session, uuid4(), AccountType.POST_PAID, one_month_ago)
    event = get_event(session)
    transaction1 = create_transaction(session, account.id, -event.price, "t1", event.id)
    transaction2 = create_transaction(session, account.id, -event.price, "t2", event.id)
    transaction3 = create_transaction(session, account.id, -event.price, "t3", event.id)


    responses.add(
        responses.POST,
        f"{EnvVars.BILLING_HOST}/invoice",
        status=200,
        json={
            "id": uuid4().__str__(),
            "user_id": uuid4().__str__(),
            "status": "Draft",
            "created_at": datetime.date.today().__str__(),
        },
    )
    responses.add(
        responses.POST,
        f"{EnvVars.BILLING_HOST}/charge",
        status=200,
        json={
            "id": uuid4().__str__(),
            "invoice_id": uuid4().__str__(),
            "status": "Progress",
            "payment_method_id": uuid4().__str__(),
            "created_at": datetime.date.today().__str__(),
        },
    )
    post_paid_automation_charge()
    responses.assert_call_count(f"{EnvVars.BILLING_HOST}/invoice", 1)
    responses.assert_call_count(f"{EnvVars.BILLING_HOST}/charge", 1)
    delete_transaction(session, transaction1.id)
    delete_transaction(session, transaction2.id)
    delete_transaction(session, transaction3.id)
    delete_account(session, account.id)
