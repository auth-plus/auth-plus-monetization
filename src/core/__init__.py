from src.core.repository.account import AccountRepository
from src.core.repository.billing import BillingService
from src.core.repository.discount import DiscountRepository
from src.core.repository.event import EventRepository
from src.core.repository.ledger import LedgerRepository
from src.core.usecase.account_create import AccountCreate
from src.core.usecase.charge_debit import ChargeDebit
from src.core.usecase.driven.creating_account import CreatingAccount
from src.core.usecase.driven.creating_charge import CreatingCharge
from src.core.usecase.driven.creating_discount import CreatingDiscount
from src.core.usecase.driven.creating_invoice import CreatingInvoice
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.fetch_billing_user import FetchBillingUser
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_discount import ReadingDiscount
from src.core.usecase.driven.reading_event import ReadingEvent
from src.core.usecase.driven.reading_transaction import ReadingTransaction
from src.core.usecase.driven.update_account import UpdateAccount
from src.core.usecase.get_total_credit import GetTotalCredit
from src.core.usecase.receive_credit import ReceiveCredit
from src.core.usecase.receive_event import ReceiveEvent
from src.core.usecase.transform_to_post_paid import TransformToPostPaid
from src.core.usecase.transform_to_pre_paid import TransformToPrePaid


class Core:
    def __init__(self):
        creating_account: CreatingAccount = AccountRepository()
        creating_charge: CreatingCharge = BillingService()
        creating_discount: CreatingDiscount = DiscountRepository()
        creating_invoice: CreatingInvoice = BillingService()
        creating_transaction: CreatingTransaction = LedgerRepository()
        fetch_billing_user: FetchBillingUser = BillingService()
        reading_account: ReadingAccount = AccountRepository()
        reading_discount: ReadingDiscount = DiscountRepository()
        reading_event: ReadingEvent = EventRepository()
        reading_transaction: ReadingTransaction = LedgerRepository()
        update_account: UpdateAccount = AccountRepository()

        account_create = AccountCreate(
            creating_account,
        )
        charge_debit = ChargeDebit(
            reading_transaction, creating_invoice, creating_charge
        )
        get_total_credit = GetTotalCredit(reading_transaction, reading_account)
        receive_credit = ReceiveCredit(
            fetch_billing_user, creating_invoice, creating_charge, creating_transaction
        )
        receive_event = ReceiveEvent(creating_transaction, reading_event)
        transform_to_post_paid = TransformToPostPaid(
            reading_transaction,
            creating_discount,
            creating_transaction,
            update_account,
            reading_account,
        )
        transform_to_pre_paid = TransformToPrePaid(
            reading_transaction,
            creating_charge,
            update_account,
            reading_discount,
            reading_account,
            creating_invoice,
        )

        self.account_create = account_create
        self.charge_debit = charge_debit
        self.get_total_credit = get_total_credit
        self.receive_credit = receive_credit
        self.receive_event = receive_event
        self.transform_to_post_paid = transform_to_post_paid
        self.transform_to_pre_paid = transform_to_pre_paid
