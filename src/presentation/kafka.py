import json

from kafka import KafkaConsumer

from src.config.envvar import EnvVars
from src.config.logger import console
from src.core import Core

topics = [
    "2FA_EMAIL_CREATED",
    "2FA_PHONE_CREATED",
    "2FA_EMAIL_SENT",
    "2FA_PHONE_SENT",
    "USER_CREATED",
    "ORGANIZATION_CREATED",
]
consumer = KafkaConsumer(
    value_deserializer=lambda m: json.loads(m.decode("ascii")),
    bootstrap_servers=[EnvVars.KAFKA_HOST],
)
consumer.subscribe(topics)


for msg in consumer:
    console.info(msg)
    core = Core()
    match msg.topic:
        case [
            "2FA_EMAIL_CREATED",
            "2FA_PHONE_CREATED",
            "2FA_EMAIL_SENT",
            "2FA_PHONE_SENT",
        ]:
            account = core.receive_event.receive_event(msg.value["external_id"])
        case "USER_CREATED":
            account = core.account_create.create(msg.value["external_id"])
        case "ORGANIZATION_CREATED":
            account = core.account_create.create(msg.value["external_id"])
