from datetime import date, time
from sqlalchemy import Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Attendance(Base):
    __tablename__ = "attendance"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False
    )
    attendance_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    check_in: Mapped[time | None] = mapped_column(
        Time,
        nullable=True
    )
    check_out: Mapped[time | None] = mapped_column(
        Time,
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(30),
        default="present"
    )