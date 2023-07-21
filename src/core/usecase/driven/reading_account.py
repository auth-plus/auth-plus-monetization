from abc import ABCMeta, abstractmethod
from uuid import UUID

from src.core.entity.account import Account


class AccountNotFoundException(Exception):
    "Raised when account does not exists on database"


class ReadingAccount(metaclass=ABCMeta):
    @abstractmethod
    def by_id(self, account_id: UUID) -> Account:
        pass

    @abstractmethod
    def by_external_id(self, external_id: UUID) -> Account:
        pass
