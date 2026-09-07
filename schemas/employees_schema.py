from pydantic import BaseModel, Field, field_validator
from datetime import date

class EmployeeCreate(BaseModel):
    department_id: int
    designation_id: int
    first_name: str = Field(
        min_length=2,
        max_length=100
    )
    last_name: str | None = Field(
        default=None,
        max_length=100
    )
    email: str | None = Field(
        default=None,
        max_length=150
    )
    phone: str | None = Field(
        default=None,
        max_length=30
    )
    hire_date: date | None = None
    @field_validator("first_name", "last_name", "email", "phone")
    @classmethod
    def clean_text(cls, value):
        if value is None:
            return value
        value = value.strip()
        if "<" in value or ">" in value:
            raise ValueError("HTML tags are not allowed")
        return value

class EmployeeUpdate(BaseModel):
    department_id: int | None = None
    designation_id: int | None = None
    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    last_name: str | None = Field(
        default=None,
        max_length=100
    )
    email: str | None = Field(
        default=None,
        max_length=150
    )
    phone: str | None = Field(
        default=None,
        max_length=30
    )
    hire_date: date | None = None
    @field_validator("first_name", "last_name", "email", "phone")
    @classmethod
    def clean_text(cls, value):
        if value is None:
            return value
        value = value.strip()
        if "<" in value or ">" in value:
            raise ValueError("HTML tags are not allowed")
        return value

class EmployeeResponse(BaseModel):
    id: int
    user_id: int | None = None
    department_id: int
    designation_id: int
    first_name: str
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    hire_date: date | None = None