from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class EventType(Enum):
    EMAIL_AUTH_FACTOR_CREATED = "EMAIL_AUTH_FACTOR_CREATED"
    PHONE_AUTH_FACTOR_CREATED = "PHONE_AUTH_FACTOR_CREATED"
    EMAIL_AUTH_FACTOR_SENT = "EMAIL_AUTH_FACTOR_SENT"
    PHONE_AUTH_FACTOR_SENT = "PHONE_AUTH_FACTOR_SENT"
    USER_CREATED = "USER_CREATED"
    ORGANIZATION_CREATED = "ORGANIZATION_CREATED"


@dataclass
class Event:
    id: UUID
    type: EventType
    price: float
    created_at: datetime


def convert_str_to_event_type(type_: str) -> EventType:
    match type_:
        case "EMAIL_AUTH_FACTOR_CREATED":
            return EventType.EMAIL_AUTH_FACTOR_CREATED
        case "PHONE_AUTH_FACTOR_CREATED":
            return EventType.PHONE_AUTH_FACTOR_CREATED
        case "EMAIL_AUTH_FACTOR_SENT":
            return EventType.EMAIL_AUTH_FACTOR_SENT
        case "PHONE_AUTH_FACTOR_SENT":
            return EventType.PHONE_AUTH_FACTOR_SENT
        case "USER_CREATED":
            return EventType.USER_CREATED
        case "ORGANIZATION_CREATED":
            return EventType.ORGANIZATION_CREATED
        case other:
            raise ValueError(f"No event mapped for this string: {other}")
