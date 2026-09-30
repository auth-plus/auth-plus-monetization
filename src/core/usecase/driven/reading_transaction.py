from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.core.entity.transaction import Transaction


class ReadingTransaction(metaclass=ABCMeta):
    @abstractmethod
    def by_account_id(
        self,
        account_id: UUID,
        date_start: datetime,
        date_end: Optional[datetime] = None,
    ) -> List[Transaction]:
        pass
