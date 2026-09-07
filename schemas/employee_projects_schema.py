from pydantic import BaseModel
from datetime import datetime

class EmployeeProjectCreate(BaseModel):
    employee_id: int
    project_id: int

class EmployeeProjectUpdate(BaseModel):
    employee_id: int | None = None
    project_id: int | None = None

class EmployeeProjectResponse(BaseModel):
    employee_id: int
    project_id: int
    assigned_at: datetime