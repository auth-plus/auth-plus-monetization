from abc import ABCMeta, abstractmethod
from uuid import UUID

from src.core.entity.discount import Discount


class ReadingDiscount(metaclass=ABCMeta):
    @abstractmethod
    def by_account_id(self, account_id: UUID) -> Discount:
        pass
