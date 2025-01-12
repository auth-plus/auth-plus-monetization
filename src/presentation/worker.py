import time
from functools import reduce

import schedule
from sqlalchemy.orm import Session

from src.config.database import engine
from src.core.entity.account import AccountType
from src.core.entity.billing import InvoiceItem
from src.core.repository.account import AccountRepository
from src.core.repository.billing import BillingService
from src.core.repository.ledger import LedgerRepository
from src.core.usecase.driven.billing.billing_updating_invoice import (
    BillingUpdatingInvoice,
)
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_transaction import ReadingTransaction


def post_paid_automation_charge():
    with Session(engine) as session:
        reading_account: ReadingAccount = AccountRepository(session)
        reading_transaction: ReadingTransaction = LedgerRepository(session)
        billing_updating_invoice: BillingUpdatingInvoice = BillingService()
        account_list = reading_account.by_subscription_period()
        for account in account_list:
            if account.type == AccountType.POST_PAID:
                transaction_list = reading_transaction.by_account_id(
                    account.id, account.created_at
                )
                amount_list = list(map(lambda a: a.amount, transaction_list))
                debit = reduce(lambda a, b: float(a + b), amount_list, 0.0)
                item = InvoiceItem("MONTHLY DEBIT", debit, "BRL", 1)
                invoice = billing_updating_invoice.add_item(account.external_id, [item])
                billing_updating_invoice.charge(invoice.id)


# Listing all jobs
schedule.every(1).day.do(post_paid_automation_charge)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
