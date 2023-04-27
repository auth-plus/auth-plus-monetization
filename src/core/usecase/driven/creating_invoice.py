from abc import ABCMeta, abstractmethod
from typing import List

from src.core.entity.billing import Invoice, InvoiceItem


class CreatingInvoice(metaclass=ABCMeta):
    @abstractmethod
    def create_invoice(self, item_list: List[InvoiceItem]) -> Invoice:
        pass
