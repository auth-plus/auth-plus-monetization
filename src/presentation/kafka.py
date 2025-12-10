import json

from kafka import (
    KafkaConsumer,
)

from src.config.envvar import EnvVars
from src.config.logger import console
from src.core import Core
from src.core.helpers import is_valid_uuid

topics = [
    "2FA_EMAIL_CREATED",
    "2FA_PHONE_CREATED",
    "2FA_EMAIL_SENT",
    "2FA_PHONE_SENT",
    "USER_CREATED",
    "ORGANIZATION_CREATED",
]
consumer = KafkaConsumer(
    topics,
    value_deserializer=lambda m: json.loads(m.decode("ascii")),
    bootstrap_servers=[EnvVars.KAFKA_HOST],
    auto_offset_reset="earliest",
    enable_auto_commit=False,
)

try:
    for msg in consumer:
        console.info(msg)
        core = Core()
        try:
            external_id = is_valid_uuid(msg.value["external_id"])
        except Exception as e:
            console.error(f"external_id UUID not valid: {e}")
            continue
        match msg.topic:
            case [
                "2FA_EMAIL_CREATED",
                "2FA_PHONE_CREATED",
                "2FA_EMAIL_SENT",
                "2FA_PHONE_SENT",
            ]:
                core.receive_event.receive_event(external_id, msg.topic)
            case "USER_CREATED":
                core.account_create.create(external_id)
            case "ORGANIZATION_CREATED":
                core.account_create.create(external_id)
except KeyboardInterrupt:
    console.warning("Stopping consumer...")
finally:
    consumer.close()
