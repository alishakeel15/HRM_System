from pydantic import BaseModel, Field, field_validator

class PermissionCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )
    description: str | None = None
    @field_validator("name", "description")
    @classmethod
    def clean_text(cls, value):
        if value is None:
            return value
        value = value.strip()
        if "<" in value or ">" in value:
            raise ValueError("HTML tags are not allowed")
        return value

class PermissionUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    description: str | None = None
    @field_validator("name", "description")
    @classmethod
    def clean_text(cls, value):
        if value is None:
            return value
        value = value.strip()
        if "<" in value or ">" in value:
            raise ValueError("HTML tags are not allowed")
        return value

class PermissionResponse(BaseModel):
    id: int
    name: str
    description: str | None = None