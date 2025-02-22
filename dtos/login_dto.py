from pydantic import BaseModel, EmailStr, field_validator

class login_user_dto(BaseModel):
    email: EmailStr
    password: str