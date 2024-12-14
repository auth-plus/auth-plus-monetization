from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class DiscountType(Enum):
    PERCENTAGE = "PERCENTAGE"
    ABSOLUTE = "ABSOLUTE"


@dataclass
class Discount:
    id: UUID
    account_id: UUID
    reason: str
    amount: float
    type: DiscountType
    created_at: datetime
    deleted_at: Optional[datetime]
