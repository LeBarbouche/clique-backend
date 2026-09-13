from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class GalleryBase(BaseModel):
    src: str = Field(min_length=1, max_length=1000)
    alt: str = Field(min_length=2, max_length=500)
    caption: str = Field(min_length=2)
    year: int = Field(ge=1900, le=2100)
    place: str = Field(min_length=2, max_length=255)


class GalleryCreate(GalleryBase):
    pass


class GalleryRead(GalleryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
