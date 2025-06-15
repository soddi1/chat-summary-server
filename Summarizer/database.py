from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Replace with your actual DB credentials
DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/yourdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Run this once to create tables
def init_db():
    Base.metadata.create_all(bind=engine)
