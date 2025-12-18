from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func

from application.database.base import Base

from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from application.database.models.transactions import Transactions
    from application.database.models.categories import Categories
    from application.database.models.tokens import Tokens

class Users(Base):
    __tablename__ = "users"

    # Base Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)

    # Service Columns
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    transactions: Mapped[list["Transactions"]] = relationship("Transactions", back_populates="user")
    categories: Mapped[list["Categories"]] = relationship("Categories", back_populates="user")
    token: Mapped["Tokens"] = relationship("Tokens", back_populates="user", cascade="all, delete-orphan")