from pydantic import BaseModel, field_validator
from typing import Optional

class comment_entity(BaseModel):
    id: Optional[int] = None
    name_user: str
    content: str
    parent_id: Optional[int] = None  
    user_id: int
    post_id: int
    is_blocked_by_post: bool = False
    is_updated: bool = False
    is_blocked: bool = False

    @field_validator("name_user", "content")
    @classmethod
    def not_blank(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError(f"{cls.__name__} field is required")
        return value
        
    @field_validator("name_user")
    @classmethod
    def size_name_user(cls, value: str):
        if len(value) > 100:
            raise ValueError("Max size for name_user is 100 characters")
        return value
        
    @field_validator("content")
    @classmethod
    def size_content(cls, value: str):
        if len(value) > 300:
            raise ValueError("Max size for content is 300 characters")
        return value
