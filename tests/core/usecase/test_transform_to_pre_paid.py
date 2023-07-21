from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4
from sqlalchemy.orm import Session

from src.core.entity.account import Account, AccountType
from src.core.entity.billing import InvoiceItem
from src.core.entity.discount import Discount, DiscountType
from src.core.entity.transaction import Transaction
from src.core.repository.account import AccountRepository
from src.core.repository.discount import DiscountRepository
from src.core.repository.ledger import LedgerRepository
from src.core.usecase.driven.billing.billing_charge import BillingCharge
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_discount import ReadingDiscount
from src.core.usecase.driven.reading_transaction import ReadingTransaction
from src.core.usecase.driven.update_account import UpdateAccount
from src.core.usecase.transform_to_pre_paid import TransformToPrePaid


def test_should_transform_to_pre_paid(session: Session):
    account_id = uuid4()
    external_id = uuid4()
    account_created_at = datetime.now()
    account = Account(
        account_id, external_id, AccountType.PRE_PAID, True, account_created_at
    )
    transaction_1 = Transaction(
        uuid4(), account_id, -1.0, "descrip", uuid4(), datetime.today()
    )
    transaction_2 = Transaction(
        uuid4(), account_id, -2.0, "descrip", uuid4(), datetime.today()
    )
    transaction_3 = Transaction(
        uuid4(), account_id, -3.0, "descrip", uuid4(), datetime.today()
    )
    discount = Discount(
        uuid4(),
        account_id,
        "PROMO",
        20.0,
        DiscountType.PERCENTAGE,
        True,
        datetime.today(),
    )
    # mock
    reading_account: ReadingAccount = AccountRepository(session)
    reading_account.by_external_id = MagicMock(return_value=account)
    reading_transaction: ReadingTransaction = LedgerRepository(session)
    reading_transaction.by_account_id = MagicMock(
        return_value=[transaction_1, transaction_2, transaction_3]
    )
    reading_discount: ReadingDiscount = DiscountRepository(session)
    reading_discount.by_account_id = MagicMock(return_value=discount)
    billing_charge: BillingCharge = LedgerRepository(session)
    billing_charge.charge = MagicMock(return_value=None)
    update_account: UpdateAccount = AccountRepository(session)
    update_account.change_type = MagicMock(return_value=None)
    # usecase
    usecase = TransformToPrePaid(
        reading_account,
        reading_transaction,
        reading_discount,
        billing_charge,
        update_account,
    )
    usecase.transform_to_pre_paid(external_id)
    # assert
    reading_account.by_external_id.assert_called_once_with(external_id)
    reading_transaction.by_account_id.assert_called_once_with(
        account_id, account_created_at
    )
    reading_discount.by_account_id.assert_called_once_with(account_id)
    billing_charge.charge.assert_called_once_with(
        external_id, [InvoiceItem("PostPaid transform", 4.8, "BRL", 1.0)]
    )
    update_account.change_type.assert_called_once_with(account_id, AccountType.PRE_PAID)
