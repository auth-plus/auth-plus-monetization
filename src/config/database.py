from sqlalchemy import create_engine

from src.config.envvar import EnvVars

engine = create_engine(EnvVars.DATABASE_HOST, echo=True)
