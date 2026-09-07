from pydantic import BaseModel, Field
from datetime import date, time

class AttendanceCreate(BaseModel):
    employee_id: int
    attendance_date: date
    check_in: time | None = None
    check_out: time | None = None
    status: str = Field(
        default="present",
        max_length=30
    )

class AttendanceUpdate(BaseModel):
    attendance_date: date | None = None
    check_in: time | None = None
    check_out: time | None = None
    status: str | None = Field(
        default=None,
        max_length=30
    )

class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    attendance_date: date
    check_in: time | None = None
    check_out: time | None = None
    status: str