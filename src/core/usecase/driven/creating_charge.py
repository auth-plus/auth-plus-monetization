from abc import ABCMeta, abstractmethod

from uuid import UUID


class CreatingCharge(metaclass=ABCMeta):
    @abstractmethod
    def create_charge(self, invoice_id: UUID):
        pass
