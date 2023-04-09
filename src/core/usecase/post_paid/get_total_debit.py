from functools import reduce
from uuid import UUID
from src.core.usecase.driven.reading_invoice import ReadingInvoice

from src.core.usecase.driven.reading_transaction import ReadingTransaction


class GetTotalDebit:
    def __init__(
        self,
        reading_transaction: ReadingTransaction,
        reading_invoice: ReadingInvoice,
    ):
        self.reading_transaction = reading_transaction
        self.reading_invoice = reading_invoice

    def get_total_debit(self, account_id: UUID) -> float:
        transaction = self.reading_transaction.get_last_transaction(account_id)
        if transaction.amount < 0:
            return 0
        else:
            invoice_item_list = self.reading_invoice.by_invoice_id(
                transaction.invoice_id
            )
            list_itens_amount = map(lambda a: a.amount, invoice_item_list)
            return reduce(lambda a, b: a + b, list_itens_amount)
