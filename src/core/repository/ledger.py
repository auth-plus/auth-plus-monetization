from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from src.core.entity.transaction import Transaction
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.reading_transaction import ReadingTransaction


class LedgerRepository(CreatingTransaction, ReadingTransaction):
    def create_transaction(self, account_id: UUID, amount: float) -> Transaction:
        new_uuid = uuid4()
        created_at = datetime.now()
        return Transaction(
            new_uuid, account_id, amount, "description", new_uuid, created_at
        )

    def by_account_id(
        self, account_id: UUID, date_start: datetime, date_end=datetime.now()
    ) -> List[Transaction]:
        pass
