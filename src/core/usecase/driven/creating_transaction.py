from abc import ABCMeta, abstractmethod

from uuid import UUID


class CreatingTransaction(metaclass=ABCMeta):
    @abstractmethod
    def create_transaction(self, account_id: UUID, amount: float):
        pass
