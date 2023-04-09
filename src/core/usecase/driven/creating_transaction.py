from abc import ABCMeta, abstractmethod
from uuid import UUID

from src.core.entity.transaction import Transaction


class CreatingTransaction(metaclass=ABCMeta):
    @abstractmethod
    def create_transaction(self, account_id: UUID, amount: float) -> Transaction:
        pass
