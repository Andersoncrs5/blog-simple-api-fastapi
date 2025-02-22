from pydantic import BaseModel, field_validator
from typing import Optional

class post_entity(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    category: str
    user_id: int
    is_blocked: bool = False

    @field_validator("title", "content", "category")
    @classmethod
    def not_blank(cls, value: str):
        if not value.strip():
            raise ValueError("This field is required")
        return value

    @field_validator("title")
    @classmethod
    def size_title(cls, value: str):
        if len(value) > 300:
            raise ValueError("Max size is 300 characters")
        return value

    @field_validator("content")
    @classmethod
    def size_content(cls, value: str):
        if len(value) > 3000:
            raise ValueError("Max size is 3000 characters")
        return value
