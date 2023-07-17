from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from src.core.entity.account import Account, AccountType
from src.core.entity.billing import Charge, Invoice, InvoiceItem
from src.core.entity.discount import Discount, DiscountType
from src.core.entity.transaction import Transaction
from src.core.repository.account import AccountRepository
from src.core.repository.discount import DiscountRepository
from src.core.repository.ledger import LedgerRepository
from src.core.usecase.driven.creating_charge import CreatingCharge
from src.core.usecase.driven.creating_invoice import CreatingInvoice
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_discount import ReadingDiscount
from src.core.usecase.driven.reading_transaction import ReadingTransaction
from src.core.usecase.driven.update_account import UpdateAccount
from src.core.usecase.transform_to_pre_paid import TransformToPrePaid


def test_should_charge_debit():
    account_id = uuid4()
    account_created_at = datetime.now()
    account = Account(
        account_id, uuid4(), AccountType.PRE_PAID, True, account_created_at
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
    invoice_id = uuid4()
    invoice = Invoice(invoice_id, account_id, "created", datetime.today())
    charge_id = uuid4()
    charge = Charge(charge_id, invoice_id, "charged", datetime.today())
    # mock
    reading_account: ReadingAccount = AccountRepository()
    reading_account.by_id = MagicMock(return_value=account)
    reading_transaction: ReadingTransaction = LedgerRepository()
    reading_transaction.by_account_id = MagicMock(
        return_value=[transaction_1, transaction_2, transaction_3]
    )
    reading_discount: ReadingDiscount = DiscountRepository()
    reading_discount.by_account_id = MagicMock(return_value=discount)
    creating_invoice: CreatingInvoice = DiscountRepository()
    creating_invoice.create_invoice = MagicMock(return_value=invoice)
    creating_charge: CreatingCharge = DiscountRepository()
    creating_charge.create_charge = MagicMock(return_value=charge)
    update_account: UpdateAccount = AccountRepository()
    update_account.change_type = MagicMock(return_value=None)
    # usecase
    usecase = TransformToPrePaid(
        reading_account,
        reading_transaction,
        reading_discount,
        creating_invoice,
        creating_charge,
        update_account,
    )
    usecase.transform_to_pre_paid(account_id)
    # assert
    reading_account.by_id.assert_called_once_with(account_id)
    reading_transaction.by_account_id.assert_called_once_with(
        account_id, account_created_at
    )
    reading_discount.by_account_id.assert_called_once_with(account_id)
    creating_invoice.create_invoice.assert_called_once_with(
        account_id, [InvoiceItem("PostPaid transform", 4.8, "BRL", 1.0)]
    )
    creating_charge.create_charge.assert_called_once_with(invoice_id)
    update_account.change_type.assert_called_once_with(account_id, AccountType.PRE_PAID)
