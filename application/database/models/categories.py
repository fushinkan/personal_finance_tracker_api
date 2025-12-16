from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey

from application.database.base import Base

from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from application.database.models.users import Users


class Categories(Base):
    __tablename__ = "categories"

    # Base Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)

    # Service Columns
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now, onupdate=func.now())

    # Relationships
    user: Mapped["Users"] = relationship("Users", back_populates="transactions")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))