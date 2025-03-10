from abc import ABCMeta, abstractmethod
from uuid import UUID

from src.core.entity.account import AccountType


class UpdatingAccount(metaclass=ABCMeta):
    @abstractmethod
    def change_type(self, account_id: UUID, type_: AccountType) -> None:
        pass
