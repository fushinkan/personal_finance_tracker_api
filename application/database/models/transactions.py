from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey, Enum

from application.database.base import Base
from features.transaction_enum import TransactionType

from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from application.database.models.users import Users


class Transactions(Base):
    __tablename__ = "transactions"

    # Base Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(nullable=False)
    category: Mapped[int] = mapped_column(String(32), nullable=False)
    description: Mapped[str | None] = mapped_column(String(512))
    transaction_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType, name="transaction_type"), nullable=False)

    # Service Columns
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now, onupdate=func.now())

    # Relationships
    user: Mapped["Users"] = relationship("Users", back_populates="categories")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))