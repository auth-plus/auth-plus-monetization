from copy import deepcopy

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Column, MetaData, Numeric, String, Table, select
from sqlalchemy.orm import Session

from src.config.database import engine
from src.core.entity.event import Event, EventType
from src.core.usecase.driven.reading_event import ReadingEvent

metadata_obj = MetaData()

event_table = Table(
    "event",
    metadata_obj,
    Column("id", SQLUUID, nullable=False),
    Column("type", String, nullable=False),
    Column("value", Numeric(5, 2), nullable=False),
    Column("created_at", TIMESTAMP),
)


class EventRepository(ReadingEvent):
    def by_type(self, type: EventType) -> Event:
        with Session(engine) as session:
            query = (
                select(event_table)
                .where(event_table.c.type == type.value)
                .order_by(event_table.c.created_at.desc())
                .limit(1)
            )
            cursor = session.execute(query).first()
            if cursor is None:
                raise Exception("event not found")
            (id, type, value, created_at) = deepcopy(cursor)
            return Event(id, type, value, created_at)
