from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from enum import Enum


class EventType(Enum):
    SPRING = 1
    SUMMER = 2
    AUTUMN = 3
    WINTER = 4


@dataclass
class Event:
    id: UUID
    type: EventType
    value: float
    created_at: datetime


def convert_str_to_event_type(type: str) -> EventType:
    match type:
        case "SPRING":
            return EventType.SPRING
        case "SUMMER":
            return EventType.SUMMER
        case "AUTUMN":
            return EventType.AUTUMN
        case "WINTER":
            return EventType.WINTER
        case other:
            raise Exception(f"No event mapped for this string: {other}")
