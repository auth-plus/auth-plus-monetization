from datetime import datetime, timedelta
from unittest.mock import MagicMock
from uuid import uuid4

from src.core.entity.billing import Charge, Invoice, InvoiceItem
from src.core.entity.transaction import Transaction
from src.core.repository.ledger import LedgerRepository
from src.core.usecase.charge_debit import ChargeDebit
from src.core.usecase.driven.creating_charge import CreatingCharge
from src.core.usecase.driven.creating_invoice import CreatingInvoice
from src.core.usecase.driven.reading_transaction import ReadingTransaction


def test_should_charge_debit():
    account_id = uuid4()
    date_start = datetime.today() - timedelta(days=1)
    date_end = datetime.now()
    transaction = Transaction(
        uuid4(), account_id, 1.0, "desc", uuid4(), datetime.today()
    )
    transaction_list = [transaction]
    invoice_item_list = list(
        map(
            lambda transac: InvoiceItem(
                transac.description, transac.amount, "BRL", 1.0
            ),
            transaction_list,
        )
    )
    invoice_id = uuid4()
    invoice = Invoice(invoice_id, account_id, "charged", datetime.today())
    charge_id = uuid4()
    charge_status = "charged"
    charge_payment_method_id = uuid4()
    charge = Charge(charge_id, invoice_id, charge_status, charge_payment_method_id)
    # mock
    reading_transaction: ReadingTransaction = LedgerRepository()
    reading_transaction.by_account_id = MagicMock(return_value=transaction_list)
    creating_invoice: CreatingInvoice = LedgerRepository()
    creating_invoice.create_invoice = MagicMock(return_value=invoice)
    creating_charge: CreatingCharge = LedgerRepository()
    creating_charge.create_charge = MagicMock(return_value=charge)
    # usecase
    usecase = ChargeDebit(reading_transaction, creating_invoice, creating_charge)
    result = usecase.charge_debit(account_id, date_start, date_end)
    # assert
    assert result.id == charge_id
    assert result.invoice_id == invoice_id
    assert result.status == charge_status
    assert result.payment_method_id == charge_payment_method_id
    reading_transaction.by_account_id.assert_called_once_with(
        account_id, date_start, date_end
    )
    creating_invoice.create_invoice.assert_called_once_with(
        account_id, invoice_item_list
    )
    creating_charge.create_charge.assert_called_once_with(invoice_id)
