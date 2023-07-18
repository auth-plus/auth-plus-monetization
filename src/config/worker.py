from celery import Celery

from src.config.envvar import EnvVars

worker = Celery("monetization-worker", broker=EnvVars.REDIS_HOST)
