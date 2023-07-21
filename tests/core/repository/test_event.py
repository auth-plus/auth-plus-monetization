from decimal import Decimal

from sqlalchemy.orm import Session

from src.core.entity.event import EventType
from src.core.repository.event import EventRepository
from tests.factory.helpers import create_event, delete_event


def test_should_select_by_type(session: Session):
    type_ = EventType.EMAIL_AUTH_FACTOR_CREATED
    price = 123.54
    event = create_event(session, type_, price)
    repository = EventRepository(session)
    result = repository.by_type(type_)
    assert result.id == event.id
    assert result.price == Decimal(str(price))
    assert result.type == type_
    assert result.created_at == event.created_at
    delete_event(session, event.id)
