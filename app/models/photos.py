from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Boolean, Integer, String, func
from app.db.database import Base

class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    photo_file_name: Mapped[str] = mapped_column(String(255), nullable=True)
    date_modified: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())  # Auto-update
    date_created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())  # Auto-set on creation
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)  # Always starts as False

    def to_dict(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
        }
