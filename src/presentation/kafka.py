import json
from typing import Any, Dict

from kafka import (
    KafkaConsumer,
)
from opentelemetry import trace

from src.config.envvar import EnvVars
from src.config.logger import console
from src.config.observability import setup_observability
from src.core import Core
from src.core.helpers import is_valid_uuid

tracer = trace.get_tracer("auth-plus-monetization-kafka")

topics = [
    "2FA_EMAIL_CREATED",
    "2FA_PHONE_CREATED",
    "2FA_EMAIL_SENT",
    "2FA_PHONE_SENT",
    "USER_CREATED",
    "ORGANIZATION_CREATED",
]


def process_message(core: Core, topic: str, value: Dict[str, Any]) -> bool:
    with tracer.start_as_current_span(f"kafka.process:{topic}") as span:
        span.set_attribute("messaging.system", "kafka")
        span.set_attribute("messaging.destination", topic)
        try:
            external_id = is_valid_uuid(value["external_id"])
            span.set_attribute("account.external_id", str(external_id))
        except Exception as e:
            console.error(f"external_id UUID not valid: {e}")
            span.record_exception(e)
            return False

        match topic:
            case (
                "2FA_EMAIL_CREATED"
                | "2FA_PHONE_CREATED"
                | "2FA_EMAIL_SENT"
                | "2FA_PHONE_SENT"
            ):
                core.receive_event.receive_event(external_id, topic)
                return True
            case "USER_CREATED" | "ORGANIZATION_CREATED":
                core.account_create.create(external_id)
                return True
            case _:
                console.warning(f"Unhandled topic: {topic}")
                return False


def start_consumer() -> None:
    setup_observability("auth-plus-monetization-kafka")
    consumer = KafkaConsumer(
        *topics,
        value_deserializer=lambda m: json.loads(m.decode("ascii")),
        bootstrap_servers=[EnvVars.KAFKA_HOST],
        auto_offset_reset="earliest",
        enable_auto_commit=False,
    )

    core = Core()
    try:
        for msg in consumer:
            console.info(msg)
            process_message(core, msg.topic, msg.value)
            consumer.commit()
    except KeyboardInterrupt:
        console.warning("Stopping consumer...")
    finally:
        consumer.close()


if __name__ == "__main__":
    start_consumer()
