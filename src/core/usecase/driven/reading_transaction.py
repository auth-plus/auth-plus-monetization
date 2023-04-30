from abc import ABCMeta, abstractmethod
from typing import List
from uuid import UUID

from src.core.entity.transaction import Transaction


class ReadingTransaction(metaclass=ABCMeta):
    @abstractmethod
    def by_account_id(self, account_id: UUID) -> List[Transaction]:
        pass

    @abstractmethod
    def get_last_transaction(self, account_id: UUID) -> Transaction:
        pass
