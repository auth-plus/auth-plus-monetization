import uuid
from typing import Any


def is_valid_uuid(value: Any):
    try:
        return uuid.UUID(str(value))
    except ValueError as exc:
        raise exc
