from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class EventType(Enum):
    EMAIL_CREATED = "2FA_EMAIL_CREATED"
    PHONE_CREATED = "2FA_PHONE_CREATED"
    EMAIL_SENT = "2FA_EMAIL_SENT"
    PHONE_SENT = "2FA_PHONE_SENT"
    USER_CREATED = "USER_CREATED"
    ORGANIZATION_CREATED = "ORGANIZATION_CREATED"


@dataclass
class Event:
    id: UUID
    type: EventType
    price: float
    created_at: datetime


def convert_str_to_event_type(type: str) -> EventType:
    match type:
        case "2FA_EMAIL_CREATED":
            return EventType.EMAIL_CREATED
        case "2FA_PHONE_CREATED":
            return EventType.PHONE_CREATED
        case "2FA_EMAIL_SENT":
            return EventType.EMAIL_SENT
        case "2FA_PHONE_SENT":
            return EventType.PHONE_SENT
        case "USER_CREATED":
            return EventType.USER_CREATED
        case "ORGANIZATION_CREATED":
            return EventType.ORGANIZATION_CREATED
        case other:
            raise Exception(f"No event mapped for this string: {other}")
