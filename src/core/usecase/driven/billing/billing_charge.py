from abc import ABCMeta, abstractmethod
from typing import List
from uuid import UUID

from src.core.entity.billing import Invoice, InvoiceItem


class BillingCharge(metaclass=ABCMeta):
    @abstractmethod
    def charge(self, external_id: UUID, item_list: List[InvoiceItem]) -> Invoice:
        pass
