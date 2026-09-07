from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal

class SalaryCreate(BaseModel):
    employee_id: int
    basic_salary: Decimal = Field(gt=0)
    allowance: Decimal = Field(default=0, ge=0)
    deduction: Decimal = Field(default=0, ge=0)
    salary_month: date

class SalaryUpdate(BaseModel):
    basic_salary: Decimal | None = Field(default=None, gt=0)
    allowance: Decimal | None = Field(default=None, ge=0)
    deduction: Decimal | None = Field(default=None, ge=0)
    salary_month: date | None = None

class SalaryResponse(BaseModel):
    id: int
    employee_id: int
    basic_salary: Decimal
    allowance: Decimal
    deduction: Decimal
    salary_month: date