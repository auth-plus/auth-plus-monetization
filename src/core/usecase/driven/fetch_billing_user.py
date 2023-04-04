from abc import ABCMeta, abstractmethod
from uuid import UUID


class FetchBillingUser(metaclass=ABCMeta):
    @abstractmethod
    def fetch_by_account_id(self, accountId: UUID):
        pass
