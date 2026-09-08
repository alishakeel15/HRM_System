from datetime import date
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime

class Leave(Base):
    __tablename__ = "leaves"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False
    )
    leave_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    status: Mapped[str] = mapped_column(
    String(20),
    default="pending",
    nullable=False
    )

    approved_by: Mapped[int | None] = mapped_column(
    ForeignKey("users.id", ondelete="SET NULL"),
    nullable=True
    )

    approved_at: Mapped[datetime | None] = mapped_column(
    DateTime,
    nullable=True
    )