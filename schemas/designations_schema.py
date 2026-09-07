from pydantic import BaseModel, Field, field_validator

class DesignationCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )
    department_id: int
    @field_validator("name")
    @classmethod
    def clean_name(cls, value):
        value = value.strip()
        if "<" in value or ">" in value:
            raise ValueError("HTML tags are not allowed")
        return value

class DesignationUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    department_id: int | None = None
    @field_validator("name")
    @classmethod
    def clean_name(cls, value):
        if value is None:
            return value
        value = value.strip()
        if "<" in value or ">" in value:
            raise ValueError("HTML tags are not allowed")
        return value

class DesignationResponse(BaseModel):
    id: int
    name: str
    department_id: int