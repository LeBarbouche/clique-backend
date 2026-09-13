from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class GalleryPhoto(Base):
    __tablename__ = "gallery_photos"

    id: Mapped[int] = mapped_column(primary_key=True)
    src: Mapped[str] = mapped_column(String(1000), nullable=False)
    alt: Mapped[str] = mapped_column(String(500), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    place: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
