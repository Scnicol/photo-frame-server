from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, Boolean, Integer, String, func

DATABASE_URL = "sqlite:///photos_database.db"  # Or change this for PostgreSQL/MySQL

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass

class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    photo_file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    date_modified: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())  # Auto-update
    date_created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())  # Auto-set on creation
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)  # Always starts as False

# Create tables in the database (if they don't already exist)
Base.metadata.create_all(engine)
