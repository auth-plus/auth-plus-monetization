import uuid
from typing import Any


def is_valid_uuid(value: Any):
    try:
        return uuid.UUID(str(value))
    except ValueError as exc:
        raise exc


class FlowPostPaidError(Exception):
    def __init__(self):
        super().__init__("This flow should only be used by post-paid plan")


class FlowPrePaidError(Exception):
    def __init__(self):
        super().__init__("This flow should only be used by pre-paid plan")
