from pydantic import BaseModel, Field, field_validator
from datetime import date

class ProjectCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=150
    )
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str = Field(
        default="active",
        max_length=50
    )
    @field_validator("name", "description", "status")
    @classmethod
    def clean_text(cls, value):
        if value is None:
            return value
        value = value.strip()
        if "<" in value or ">" in value:
            raise ValueError("HTML tags are not allowed")
        return value

class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = Field(
        default=None,
        max_length=50
    )
    @field_validator("name", "description", "status")
    @classmethod
    def clean_text(cls, value):
        if value is None:
            return value
        value = value.strip()
        if "<" in value or ">" in value:
            raise ValueError("HTML tags are not allowed")
        return value

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str