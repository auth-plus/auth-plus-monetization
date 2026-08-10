import logging

import uptrace
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.instrumentation.kafka import KafkaInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.logging.handler import LoggingHandler
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

from src.config.envvar import EnvVars


def setup_observability(service_name: str):
    uptrace.configure_opentelemetry(
        dsn=EnvVars.UPTRACE_DSN,
        service_name=service_name,
        service_version="0.1.0",
    )
    # Apply global instrumentations
    LoggingInstrumentor().instrument(set_logging_format=True)
    RequestsInstrumentor().instrument()
    KafkaInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument()

    # Forward Python logging records to Uptrace via OTLP
    logger_provider = LoggerProvider(
        resource=Resource.create({"service.name": service_name})
    )
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(
            OTLPLogExporter(
                endpoint=EnvVars.UPTRACE_DSN,
                insecure=True,
            )
        )
    )
    log_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
    logging.getLogger("uvicorn.access").addHandler(log_handler)
    logging.getLogger(EnvVars.APP_NAME).addHandler(log_handler)
