from abc import ABCMeta, abstractmethod
from uuid import UUID


class UpdatingTransaction(metaclass=ABCMeta):
    @abstractmethod
    def add_charge(self, account_id: UUID, charge_id: UUID) -> None:
        pass
