from abc import ABCMeta, abstractmethod
from uuid import UUID

from src.core.entity.account import Account


class ReadingAccount(metaclass=ABCMeta):
    @abstractmethod
    def by_id(self, account_id: UUID) -> Account:
        pass
