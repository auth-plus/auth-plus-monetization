from copy import deepcopy
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session

from src.config.database import engine
from src.core.entity.account import AccountType
from src.core.entity.event import EventType
from src.core.repository.event import EventRepository, event_table

from tests.factory.helpers import create_event, delete_event


def test_should_select_by_type(session: Session):
    type = EventType.EMAIL_CREATED
    price = 123.54
    event = create_event(session, type, price)
    repository = EventRepository(session)
    result = repository.by_type(type)
    assert result.id == event.id
    assert result.price == Decimal(str(price))
    assert result.type == type
    assert result.created_at == event.created_at
    delete_event(session, event.id)
