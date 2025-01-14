from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class AccountType(Enum):
    PRE_PAID = "PRE_PAID"
    POST_PAID = "POST_PAID"


@dataclass
class Account:
    id: UUID
    external_id: UUID
    type: AccountType
    created_at: datetime
    deleted_at: Optional[datetime]
