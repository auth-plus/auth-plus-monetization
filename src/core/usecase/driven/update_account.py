from abc import ABCMeta, abstractmethod
from uuid import UUID

from src.core.entity.account import AccountType
from src.core.entity.transaction import Transaction


class UpdateAccount(metaclass=ABCMeta):
    @abstractmethod
    def change_type(self, account_id: UUID, type: AccountType) -> Transaction:
        pass
