from abc import ABCMeta, abstractmethod
from typing import List
from uuid import UUID

from src.core.entity.billing import InvoiceItem


class ReadingInvoice(metaclass=ABCMeta):
    @abstractmethod
    def by_invoice_id(self, invoice_id: UUID) -> List[InvoiceItem]:
        pass
