from datetime import date
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    start_date: Mapped[date | None] = mapped_column(
        nullable=True
    )
    end_date: Mapped[date | None] = mapped_column(
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="active"
    )