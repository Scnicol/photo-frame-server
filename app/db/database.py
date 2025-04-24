# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, DeclarativeBase

# DATABASE_URL = "sqlite:///instance/photos.db"

# engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# class Base(DeclarativeBase):
#     pass

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
