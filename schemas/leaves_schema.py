from pydantic import BaseModel, Field, field_validator
from datetime import date

class LeaveCreate(BaseModel):
    employee_id: int
    leave_type: str = Field(
        min_length=2,
        max_length=50
    )
    start_date: date
    end_date: date
    reason: str | None = None
    status: str = Field(
        default="pending",
        max_length=30
    )
    @field_validator("leave_type", "reason", "status")
    @classmethod
    def clean_text(cls, value):
        if value is None:
            return value
        value = value.strip()
        if "<" in value or ">" in value:
            raise ValueError("HTML tags are not allowed")
        return value

class LeaveUpdate(BaseModel):
    leave_type: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )
    start_date: date | None = None
    end_date: date | None = None
    reason: str | None = None
    status: str | None = Field(
        default=None,
        max_length=30
    )
    @field_validator("leave_type", "reason", "status")
    @classmethod
    def clean_text(cls, value):
        if value is None:
            return value
        value = value.strip()
        if "<" in value or ">" in value:
            raise ValueError("HTML tags are not allowed")
        return value

class LeaveResponse(BaseModel):
    id: int
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str | None = None
    status: str