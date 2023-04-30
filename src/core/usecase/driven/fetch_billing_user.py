from abc import ABCMeta, abstractmethod
from uuid import UUID

from src.core.entity.billing import BillingUser


class FetchBillingUser(metaclass=ABCMeta):
    @abstractmethod
    def fetch_by_account_id(self, accountId: UUID) -> BillingUser:
        pass
