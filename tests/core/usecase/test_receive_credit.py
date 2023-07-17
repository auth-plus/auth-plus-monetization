from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from src.core.entity.account import Account, AccountType
from src.core.entity.billing import Charge, Invoice, InvoiceItem
from src.core.repository.billing import BillingService
from src.core.repository.ledger import LedgerRepository
from src.core.usecase.driven.creating_charge import CreatingCharge
from src.core.usecase.driven.creating_invoice import CreatingInvoice
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.fetch_billing_user import FetchBillingUser
from src.core.usecase.receive_credit import ReceiveCredit


def test_should_charge_debit():
    account_id = uuid4()
    amount = 100.99
    account = Account(account_id, uuid4(), AccountType.PRE_PAID, True, datetime.now())
    invoice_id = uuid4()
    invoice = Invoice(invoice_id, account_id, "charged", datetime.today())
    charge_id = uuid4()
    charge_payment_method_id = uuid4()
    charge = Charge(charge_id, invoice_id, "charged", charge_payment_method_id)
    # mock
    fetch_billing_user: FetchBillingUser = BillingService()
    fetch_billing_user.fetch_by_account_id = MagicMock(return_value=account)
    creating_invoice: CreatingInvoice = BillingService()
    creating_invoice.create_invoice = MagicMock(return_value=invoice)
    creating_charge: CreatingCharge = BillingService()
    creating_charge.create_charge = MagicMock(return_value=charge)
    creating_transaction: CreatingTransaction = LedgerRepository()
    creating_transaction.create_transaction = MagicMock(return_value=None)
    # usecase
    usecase = ReceiveCredit(
        fetch_billing_user, creating_invoice, creating_charge, creating_transaction
    )
    result = usecase.receive_credit(account_id, amount)
    # assert
    assert result.id == charge_id
    assert result.invoice_id == invoice_id
    assert result.payment_method_id == charge_payment_method_id
    assert result.status == "charged"
    fetch_billing_user.fetch_by_account_id.assert_called_once_with(account_id)
    creating_invoice.create_invoice.assert_called_once_with(
        account_id, [InvoiceItem("CREDIT", amount, "BRL", 1.0)]
    )
    creating_charge.create_charge.assert_called_once_with(invoice_id)
    creating_transaction.create_transaction.assert_called_once_with(account_id, amount)
