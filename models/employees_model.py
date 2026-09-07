from datetime import date
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        unique=True,
        nullable=True
    )
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="RESTRICT"),
        nullable=False
    )
    designation_id: Mapped[int] = mapped_column(
        ForeignKey("designations.id", ondelete="RESTRICT"),
        nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    email: Mapped[str | None] = mapped_column(
        String(150),
        unique=True,
        nullable=True
    )
    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )
    hire_date: Mapped[date | None] = mapped_column(
        nullable=True
    )