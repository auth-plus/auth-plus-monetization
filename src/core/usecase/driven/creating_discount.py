from abc import ABCMeta, abstractmethod
from uuid import UUID

from src.core.entity.discount import Discount, DiscountType


class CreatingDiscount(metaclass=ABCMeta):
    @abstractmethod
    def create_discount(
        self, account_id: UUID, reason: str, amount: float, type: DiscountType
    ) -> Discount:
        pass
