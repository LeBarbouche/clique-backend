from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContactCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    message: str = Field(min_length=10, max_length=5000)


class ContactRead(ContactCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    is_read: bool
