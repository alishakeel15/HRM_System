from datetime import date
from decimal import Decimal
from sqlalchemy import Date, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Salary(Base):
    __tablename__ = "salaries"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False
    )
    basic_salary: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )
    allowance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0
    )
    deduction: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0
    )
    salary_month: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )