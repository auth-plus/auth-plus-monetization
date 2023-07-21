from copy import deepcopy

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Column, Enum, MetaData, Numeric, Table, select
from sqlalchemy.orm import Session

from src.core.entity.event import Event, EventType
from src.core.usecase.driven.reading_event import ReadingEvent

metadata_obj = MetaData()

event_table = Table(
    "event",
    metadata_obj,
    Column("id", SQLUUID, nullable=False),
    Column("type", Enum(EventType), nullable=False),
    Column("price", Numeric(5, 2), nullable=False),
    Column("created_at", TIMESTAMP),
)


class EventRepository(ReadingEvent):
    def __init__(self, session: Session):
        self.session = session

    def by_type(self, type: EventType) -> Event:
        query = (
            select(event_table)
            .where(event_table.c.type == type)
            .order_by(event_table.c.created_at.desc())
            .limit(1)
        )
        cursor = self.session.execute(query).first()
        if cursor is None:
            raise Exception("event not found")
        (id, type, price, created_at) = deepcopy(cursor)
        return Event(id, type, price, created_at)
