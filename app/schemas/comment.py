from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    content_type: str = Field(pattern="^(news|photo|event)$")
    content_id: int = Field(gt=0)
    body: str = Field(min_length=1, max_length=2000)


class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content_type: str
    content_id: int
    author_id: int
    body: str
    created_at: datetime