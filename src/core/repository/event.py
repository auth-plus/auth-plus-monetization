from src.core.entity.event import Event, EventType
from src.core.usecase.driven.reading_event import ReadingEvent


class EventRepository(ReadingEvent):
    def by_type(self, type: EventType) -> Event:
        pass
