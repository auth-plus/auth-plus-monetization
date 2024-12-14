from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from src.core.entity.event import EventType
from src.core.repository.price import PriceRepository


def test_should_select_by_type(session: Session):
    type_ = EventType.EMAIL_AUTH_FACTOR_CREATED
    repository = PriceRepository(session)
    result = repository.by_event(type_)
    assert isinstance(result.id, UUID)
    assert isinstance(result.price, Decimal)
    assert result.type == type_
    assert isinstance(result.created_at, datetime)
