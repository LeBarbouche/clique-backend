from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class EventBase(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    date: date
    start_time: str = Field(pattern=r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    end_time: str | None = Field(default=None, pattern=r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    venue: str = Field(min_length=2, max_length=255)
    city: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=2)
    category: str = Field(min_length=2, max_length=50)
    is_free: bool = True


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
