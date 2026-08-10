import logging
from contextvars import ContextVar

from src.config.envvar import EnvVars

request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")


class ContextFormatter(logging.Formatter):
    def format(self, record):
        # Inject defaults for missing custom attributes
        if not hasattr(record, "request_id"):
            record.request_id = request_id_ctx.get() or "N/A"
        if not hasattr(record, "trace_id"):
            # LoggingInstrumentor exposes otelTraceID / otelSpanID
            record.trace_id = getattr(record, "otelTraceID", "N/A") or "N/A"
        return super().format(record)


FORMAT = ContextFormatter(
    "[%(asctime)s] [%(levelname)s] [request_id=%(request_id)s] "
    "[trace_id=%(trace_id)s] %(message)s"
)
handler = logging.StreamHandler()
handler.setFormatter(FORMAT)
logging.getLogger("uvicorn.access").addHandler(handler)

console = logging.getLogger(EnvVars.APP_NAME)
console.addHandler(handler)
console.setLevel(logging.INFO)
console.propagate = False
