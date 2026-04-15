import logging

from src.config.envvar import EnvVars

FORMAT = "%(asctime)s %(levelname)s: %(message)s"
logging.basicConfig(format=FORMAT)
console = logging.getLogger(EnvVars.APP_NAME)
