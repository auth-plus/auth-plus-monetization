from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Discount:
    id: UUID
    account_id: UUID
    reason: str
    amount: float
    is_enable: bool
    created_at: datetime
