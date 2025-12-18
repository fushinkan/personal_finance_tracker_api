from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, func, ForeignKey

from application.database.base import Base

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.database.models.users import Users

class Tokens(Base):
    __tablename__ = "tokens"

    # Base Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str]

    # Service Columns
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user: Mapped["Users"] = relationship("Users", back_populates="token")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))