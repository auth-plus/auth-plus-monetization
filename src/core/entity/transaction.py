from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Transaction:
    id: UUID
    account_id: UUID
    amount: float
    description: str
    event_id: UUID
    created_at: datetime
