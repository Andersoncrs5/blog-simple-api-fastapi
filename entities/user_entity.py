from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class user_entity(BaseModel):
    id: Optional[int] = None
    name: str = "user"
    email: EmailStr
    password: str = "12345678"
    is_adm: bool = False
    is_block: bool = False
    
    @field_validator("name", "email", "password")
    @classmethod
    def not_blank(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("This field is required")
        return value
        
    @field_validator("name")
    @classmethod
    def size_name(cls, value: str):
        if len(value) > 100:
            raise ValueError("Max size is 100")
        return value
        
    @field_validator("email")
    @classmethod
    def size_email(cls, value: str):
        if len(value) > 150:
            raise ValueError("Max size is 150")
        return value
        
    @field_validator("password")
    @classmethod
    def size_password(cls, value: str):
        if len(value) > 100:
            raise ValueError("Max size is 100")
        return value
