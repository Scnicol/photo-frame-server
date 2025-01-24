from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime, func, Boolean, create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

#Creating the class with tablename and columns
class Photo(Base):
    __tablename__ = 'photos'
    id: Mapped[int] = mapped_column(primary_key=True)
    photo_file_name: Mapped[str] = mapped_column(String(30))
    date_modified: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    date_created: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

DATABASE_URL = "sqlite:///photo_server.db"
engine = create_engine(DATABASE_URL, echo=True)

if __name__ == "__main__":

    Base.metadata.create_all(engine)
    print("Database has been created")

#Delete files from the file system on the Raspberry Pi

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, photo_file_name={self.photo_file_name!r})"
