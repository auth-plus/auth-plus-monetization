from uuid import UUID

from src.config.logger import console
from src.core.entity.account import Account, AccountType
from src.core.usecase.driven.creating_account import CreatingAccount


class AccountCreate:
    def __init__(
        self,
        creating_account: CreatingAccount,
    ):
        self.creating_account = creating_account

    def create(self, external_id: UUID, type=AccountType.PRE_PAID) -> Account:
        console.info(f"Creating account for external_id={external_id} with type={type}")
        account = self.creating_account.create(external_id, type)
        console.info(f"Successfully created account {account.id}")
        return account
