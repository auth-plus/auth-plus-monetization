from huey import RedisHuey

from src.config.envvar import EnvVars

huey = RedisHuey(EnvVars.APP_NAME, host=EnvVars.REDIS_HOST)
