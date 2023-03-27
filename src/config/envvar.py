import os


def get_env():
    env = {
        "app": {
            "name": os.getenv("APP_NAME"),
            "port": os.getenv("PORT"),
            "enviroment": os.getenv("PYTHON_ENV"),
        }
    }
    return env
