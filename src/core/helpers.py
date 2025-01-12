import uuid
from typing import Any


def is_valid_uuid(value: Any):
    return uuid.UUID(str(value))


class FlowPostPaidError(Exception):
    def __init__(self):
        super().__init__("This flow should only be used by post-paid plan")


class FlowPrePaidError(Exception):
    def __init__(self):
        super().__init__("This flow should only be used by pre-paid plan")


class InvoicePostPaidError(Exception):
    def __init__(self):
        super().__init__("Every post-paid user should have at least a draft invoice")
