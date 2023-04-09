from abc import ABCMeta, abstractmethod
from uuid import UUID

from src.core.entity.billing import Invoice


class CreatingInvoiceItem(metaclass=ABCMeta):
    @abstractmethod
    def create_invoice_item(
        self,
        invoice_id: UUID,
        description: str,
        amount: float,
        currency: str,
        quantity: float,
    ) -> Invoice:
        pass
