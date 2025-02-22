from pydantic import BaseModel, field_validator
from typing import Optional

class like_entity(BaseModel):
    id: Optional[int] = None
    user_id: int
    post_id: int

    @field_validator("user_id", "post_id")
    @classmethod
    def must_be_positive(cls, value: int):
        if value <= 0:
            raise ValueError(f"{cls.__name__}: {value} should be positive and different from 0")
        return value
