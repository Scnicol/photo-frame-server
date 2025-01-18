from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

#creating the class with tablename and columns
class Photo(Base):
    __tablename__ = 'photos'
    id: Mapped[int] = mapped_column(primary_key=True)
    photo_file_name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, photo_file_name={self.photo_file_name!r})"
