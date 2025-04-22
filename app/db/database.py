from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///instance/photos.db"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# Create tables in the database (if they don't already exist)
Base = declarative_base()
