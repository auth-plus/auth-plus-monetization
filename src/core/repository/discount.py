from uuid import UUID

from src.core.entity.discount import Discount
from src.core.usecase.driven.creating_discount import CreatingDiscount
from src.core.usecase.driven.reading_discount import ReadingDiscount


class DiscountRepository(CreatingDiscount, ReadingDiscount):
    def create_discount(self, account_id: UUID, reason: str, amount: float) -> Discount:
        pass

    def by_account_id(self, account_id: UUID) -> Discount:
        pass
