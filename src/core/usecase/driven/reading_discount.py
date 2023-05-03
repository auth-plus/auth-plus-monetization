from abc import ABCMeta, abstractmethod
from typing import List
from uuid import UUID

from src.core.entity.account import Discount


class ReadingDiscount(metaclass=ABCMeta):
    @abstractmethod
    def by_account_id(self, account_id: UUID) -> List[Discount]:
        pass

    @abstractmethod
    def get_total_absolute(self, account_id: UUID) -> float:
        pass
