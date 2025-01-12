from abc import ABCMeta, abstractmethod
from typing import List
from uuid import UUID

from src.core.entity.billing import Charge, Invoice, InvoiceItem


class BillingUpdatingInvoice(metaclass=ABCMeta):
    @abstractmethod
    def charge(self, invoice_id: UUID) -> Charge:
        pass

    @abstractmethod
    def add_item(self, external_id: UUID, item_list: List[InvoiceItem]) -> Invoice:
        pass
