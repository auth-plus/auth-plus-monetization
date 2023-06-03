from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://root:db_password@localhost:5432/monetization", echo=True
)
