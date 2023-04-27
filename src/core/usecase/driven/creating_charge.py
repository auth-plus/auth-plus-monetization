from abc import ABCMeta, abstractmethod
from uuid import UUID

from src.core.entity.billing import Charge


class CreatingCharge(metaclass=ABCMeta):
    @abstractmethod
    def create_charge(self, invoice_id: UUID) -> Charge:
        pass
