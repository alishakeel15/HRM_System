from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=100
    )
    email: str = Field(
        max_length=150
    )
    password: str = Field(
        min_length=8
    )
    is_active: bool = True
    @field_validator("username", "email", "password")
    @classmethod
    def clean_text(cls, value):
        value = value.strip()
        if "<" in value or ">" in value:
            raise ValueError("HTML tags are not allowed")
        return value

class UserUpdate(BaseModel):
    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )
    email: str | None = Field(
        default=None,
        max_length=150
    )
    password: str | None = Field(
        default=None,
        min_length=8
    )
    is_active: bool | None = None
    @field_validator("username", "email", "password")
    @classmethod
    def clean_text(cls, value):
        if value is None:
            return value
        value = value.strip()
        if "<" in value or ">" in value:
            raise ValueError("HTML tags are not allowed")
        return value

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role_id: int | None = None
    is_active: bool
    created_at: datetime

class ChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)

class ForgotPassword(BaseModel):
    email: str

class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8)

class UserRoleUpdate(BaseModel):
    role_id: int