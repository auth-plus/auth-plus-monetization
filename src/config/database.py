from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://root:db_password@database:5432/monetization", echo=True
)
