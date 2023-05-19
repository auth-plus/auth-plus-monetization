from abc import ABCMeta, abstractmethod

from src.core.entity.event import Event, EventType


class ReadingEvent(metaclass=ABCMeta):
    @abstractmethod
    def by_type(self, type: EventType) -> Event:
        pass
