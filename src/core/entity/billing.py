from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class BillingUser:
    id: UUID
    external_id: UUID


@dataclass
class InvoiceItem:
    description: str
    amount: float
    currency: str
    quantity: float


@dataclass
class Charge:
    id: UUID
    invoice_id: UUID
    status: str
    payment_method_id: UUID


@dataclass
class Invoice:
    id: UUID
    user_id: UUID
    status: str
    created_at: datetime
