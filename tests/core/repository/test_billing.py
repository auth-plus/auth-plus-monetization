from uuid import uuid4

import responses
from sqlalchemy.orm import Session

from src.config.envvar import EnvVars
from src.core.entity.account import AccountType
from src.core.repository.billing import BillingService
from tests.factory.helpers import create_account, delete_account


@responses.activate
def test_should_fetch_user(session: Session):
    account = create_account(session, uuid4(), AccountType.PRE_PAID)
    responses.add(
        responses.GET,
        f"{EnvVars.BILLING_HOST}/user/{account.external_id}",
        status=200,
        json={
            "id": str(uuid4()),
            "external_id": str(account.external_id),
        },
    )
    repository = BillingService()
    repository.fetch_by_account_id(account.external_id)
    responses.assert_call_count(f"{EnvVars.BILLING_HOST}/user/{account.external_id}", 1)
    delete_account(session, account.id)
