from abc import ABCMeta, abstractmethod
from uuid import UUID

from src.core.entity.billing import Invoice


class BillingFetchingInvoice(metaclass=ABCMeta):
    @abstractmethod
    def get_current(self, external_id: UUID) -> Invoice:
        pass
