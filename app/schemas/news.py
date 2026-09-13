from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NewsBase(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    slug: str = Field(min_length=2, max_length=255, pattern=r"^[a-z0-9-]+$")
    content: str = Field(min_length=2)
    image_url: str | None = Field(default=None, max_length=1000)
    published: bool = False


class NewsCreate(NewsBase):
    pass


class NewsRead(NewsBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime