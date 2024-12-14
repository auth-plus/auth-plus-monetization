from copy import deepcopy

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Column, Enum, MetaData, Numeric, Table, select
from sqlalchemy.orm import Session

from src.core.entity.event import Event, EventType
from src.core.usecase.driven.reading_event import EventNotFoundException, ReadingEvent

metadata_obj = MetaData()

event_table = Table(
    "price",
    metadata_obj,
    Column("id", SQLUUID, nullable=False),
    Column("event", Enum(EventType), nullable=False),
    Column("value", Numeric(5, 2), nullable=False),
    Column("created_at", TIMESTAMP, nullable=False),
    Column("deleted_at", TIMESTAMP),
)


class PriceRepository(ReadingEvent):
    def __init__(self, session: Session):
        self.session = session

    def by_event(self, event: EventType) -> Event:
        query = (
            select(event_table)
            .where(event_table.c.event == event)
            .order_by(event_table.c.created_at.desc())
            .limit(1)
        )
        cursor = self.session.execute(query).first()
        if cursor is None:
            raise EventNotFoundException("event not found")
        (id_, event_, price, created_at, deleted_at) = deepcopy(cursor)
        return Event(id_, event_, price, created_at)
