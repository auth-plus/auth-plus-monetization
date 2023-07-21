from abc import ABCMeta, abstractmethod

from src.core.entity.event import Event, EventType


class EventNotFoundException(Exception):
    "Raised when event does not exists on database"
    pass


class ReadingEvent(metaclass=ABCMeta):
    @abstractmethod
    def by_type(self, type: EventType) -> Event:
        pass
