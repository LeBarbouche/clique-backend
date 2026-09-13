from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MemberBase(BaseModel):
    first_name: str = Field(min_length=2, max_length=120)
    last_name: str = Field(min_length=2, max_length=120)
    instrument: str = Field(min_length=2, max_length=120)
    section: str = Field(min_length=2, max_length=50)
    joined_year: int = Field(ge=1900, le=2100)
    role: str | None = Field(default=None, max_length=120)


class MemberCreate(MemberBase):
    pass


class MemberRead(MemberBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
