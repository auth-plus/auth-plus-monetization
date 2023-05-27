from datetime import datetime
from uuid import UUID

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Boolean, DateTime, String, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from src.config.database import engine
from src.core.entity.account import Account, AccountType
from src.core.usecase.driven.creating_account import CreatingAccount
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.update_account import UpdateAccount


class AccountDao:
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[UUID] = mapped_column(SQLUUID())
    type: Mapped[AccountType] = mapped_column(String(20))
    is_enable: Mapped[bool] = mapped_column(Boolean())
    created_at: Mapped[datetime] = mapped_column(DateTime())


class AccountRepository(CreatingAccount, ReadingAccount, UpdateAccount):
    def create(self, external_id: UUID, type: AccountType) -> Account:
        with Session(engine) as session:
            insert_line = AccountDao(external_id=external_id, type=type, is_enable=True)
            session.add(insert_line)
            session.flush()
            return Account(
                insert_line.id, external_id, type, True, insert_line.created_at
            )

    def by_id(self, account_id: UUID) -> Account:
        with Session(engine) as session:
            row = select(AccountDao).where(AccountDao.id == account_id).limit(1)
            print(row)

    def change_type(self, account_id: UUID, type: AccountType) -> None:
        pass
