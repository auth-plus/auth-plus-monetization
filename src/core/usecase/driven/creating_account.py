from abc import ABCMeta, abstractmethod
from uuid import UUID

from src.core.entity.account import Account, AccountType


class CreatingAccount(metaclass=ABCMeta):
    @abstractmethod
    def create(self, external_id: UUID, type_: AccountType) -> Account:
        pass
