from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class AccountType(Enum):
    PRE_PAID = "PRE_PAID"
    POST_PAID_MONTH = "POST_PAID_MONTH"
    POST_PAID_SEMESTER = "POST_PAID_SEMESTER"
    POST_PAID_ANNUAL = "POST_PAID_ANNUAL"


@dataclass
class Subscription:
    id: UUID
    type: AccountType
    created_at: datetime
    deleted_at: Optional[datetime]


@dataclass
class Account:
    id: UUID
    subscription: Subscription
    external_id: UUID
    created_at: datetime
    deleted_at: Optional[datetime]
