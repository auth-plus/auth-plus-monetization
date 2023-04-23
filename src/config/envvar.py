import os
from typing import Optional, TypedDict


class AppVars(TypedDict):
    name: Optional[str]
    port: Optional[str]
    environment: Optional[str]


class EnvVars(TypedDict):
    app: AppVars


def get_env() -> EnvVars:
    return {
        "app": {
            "name": os.getenv("APP_NAME"),
            "port": os.getenv("PORT"),
            "environment": os.getenv("PYTHON_ENV"),
        }
    }
