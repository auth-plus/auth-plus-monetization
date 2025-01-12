import os

from dotenv import load_dotenv

load_dotenv()


class EnvVars:
    APP_NAME = os.getenv("APP_NAME")
    APP_PORT = os.getenv("PORT")
    APP_ENV = os.getenv("PYTHON_ENV")
    DATABASE_HOST = os.environ["DATABASE_URL"]
    KAFKA_HOST = os.environ["KAFKA_URL"]
    BILLING_HOST = "http://localhost:5002"
