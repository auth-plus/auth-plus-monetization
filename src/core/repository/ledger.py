from datetime import datetime
from uuid import UUID, uuid4
from src.core.entity.transaction import Transaction
from src.core.usecase.driven.creating_transaction import CreatingTransaction


class Ledger(CreatingTransaction):
    __billing_endpoint = "localhost:5002"

    def create_transaction(self, account_id: UUID, amount: float) -> Transaction:
        new_uuid = uuid4()
        created_at = datetime.now()
        return Transaction(new_uuid, account_id, amount, new_uuid, created_at)
