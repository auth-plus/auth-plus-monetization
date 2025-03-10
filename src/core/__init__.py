from sqlalchemy.orm import Session

from src.config.database import engine
from src.core.repository.account import AccountRepository
from src.core.repository.billing import BillingService
from src.core.repository.discount import DiscountRepository
from src.core.repository.ledger import LedgerRepository
from src.core.repository.price import PriceRepository
from src.core.usecase.account_create import AccountCreate
from src.core.usecase.charge_debit import ChargeDebit
from src.core.usecase.driven.billing.billing_fetch_user import BillingFetchUser
from src.core.usecase.driven.billing.billing_fetching_invoice import (
    BillingFetchingInvoice,
)
from src.core.usecase.driven.billing.billing_updating_invoice import (
    BillingUpdatingInvoice,
)
from src.core.usecase.driven.creating_account import CreatingAccount
from src.core.usecase.driven.creating_discount import CreatingDiscount
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_discount import ReadingDiscount
from src.core.usecase.driven.reading_event import ReadingEvent
from src.core.usecase.driven.reading_transaction import ReadingTransaction
from src.core.usecase.driven.update_account import UpdatingAccount
from src.core.usecase.driven.update_transaction import UpdatingTransaction
from src.core.usecase.get_total_credit import GetTotalCredit
from src.core.usecase.receive_credit import ReceiveCredit
from src.core.usecase.receive_event import ReceiveEvent
from src.core.usecase.transform_to_post_paid import TransformToPostPaid
from src.core.usecase.transform_to_pre_paid import TransformToPrePaid


class Core:
    def __init__(self):
        with Session(engine) as session:
            billing_updating_invoice: BillingUpdatingInvoice = BillingService()
            billing_fetch_user: BillingFetchUser = BillingService()
            billing_fetching_invoice: BillingFetchingInvoice = BillingService()
            creating_account: CreatingAccount = AccountRepository(session)
            creating_discount: CreatingDiscount = DiscountRepository(session)
            creating_transaction: CreatingTransaction = LedgerRepository(session)
            reading_account: ReadingAccount = AccountRepository(session)
            reading_discount: ReadingDiscount = DiscountRepository(session)
            reading_event: ReadingEvent = PriceRepository(session)
            reading_transaction: ReadingTransaction = LedgerRepository(session)
            updating_account: UpdatingAccount = AccountRepository(session)
            updating_transaction: UpdatingTransaction = LedgerRepository(session)

            account_create = AccountCreate(
                creating_account,
            )
            charge_debit = ChargeDebit(
                reading_account,
                billing_updating_invoice,
                billing_fetching_invoice,
                updating_transaction,
            )
            get_total_credit = GetTotalCredit(reading_account, reading_transaction)
            receive_credit = ReceiveCredit(
                reading_account,
                billing_fetch_user,
                billing_updating_invoice,
                creating_transaction,
            )
            receive_event = ReceiveEvent(
                reading_event,
                reading_account,
                creating_transaction,
                billing_updating_invoice,
            )
            transform_to_post_paid = TransformToPostPaid(
                reading_account,
                reading_transaction,
                creating_discount,
                updating_account,
            )
            transform_to_pre_paid = TransformToPrePaid(
                reading_account,
                reading_transaction,
                reading_discount,
                billing_updating_invoice,
                updating_account,
            )

            self.account_create = account_create
            self.charge_debit = charge_debit
            self.get_total_credit = get_total_credit
            self.receive_credit = receive_credit
            self.receive_event = receive_event
            self.transform_to_post_paid = transform_to_post_paid
            self.transform_to_pre_paid = transform_to_pre_paid
