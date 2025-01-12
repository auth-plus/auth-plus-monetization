from abc import ABCMeta, abstractmethod
from uuid import UUID

from src.core.entity.billing import Invoice


class NoDraftInvoiceFound(Exception):
    "Raised when account does not exists on database"


class BillingFetchingInvoice(metaclass=ABCMeta):
    @abstractmethod
    def get_current(self, external_id: UUID) -> Invoice:
        pass
