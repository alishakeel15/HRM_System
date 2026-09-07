from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class RevokedToken(Base):
    __tablename__ = "revoked_tokens"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    token: Mapped[str] = mapped_column(
        String(1000),
        unique=True,
        nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    revoked_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )