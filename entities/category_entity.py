from pydantic import BaseModel, field_validator
from typing import Optional

class category_entity(BaseModel):
    id: Optional[int] = None
    name: str
    name_user: str
    is_actived: bool = True
    user_id: int

    @field_validator("name", "name_user")
    @classmethod
    def not_blank(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError(f"{cls.__name__} field is required")
        return value

    @field_validator("name")
    @classmethod
    def size_name(cls, value: str):
        if len(value) > 150:
            raise ValueError("Max size for name is 150 characters")
        return value
        
    @field_validator("name_user")
    @classmethod
    def size_name_user(cls, value: str):
        if len(value) > 100:
            raise ValueError("Max size for name_user is 100 characters")
        return value
