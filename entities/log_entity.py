from pydantic import BaseModel, field_validator
from typing import Optional
from enum import Enum

class TargetTypeEnum(str, Enum):
    post = 'post'
    comment = 'comment'
    user = 'user'

class log_entity(BaseModel):
    id: Optional[int] = None
    admin_id: int
    action: str
    target_id: int
    target_type: TargetTypeEnum

    @field_validator("action", "target_type")
    @classmethod
    def not_blank(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError(f"{cls.__name__} field is required")
        return value

    @field_validator("action")
    @classmethod
    def size_action(cls, value: str):
        if len(value) > 255:
            raise ValueError("Max size for action is 255 characters")
        return value
