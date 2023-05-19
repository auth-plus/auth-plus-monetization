from uuid import UUID

from src.core.entity.account import Account, AccountType
from src.core.usecase.driven.creating_account import CreatingAccount


class AccountCreate:
    def __init__(
        self,
        creating_account: CreatingAccount,
    ):
        self.creating_account = creating_account

    def create(self, external_id: UUID, type: AccountType) -> Account:
        account = self.creating_account.create(external_id, type)
        return account
