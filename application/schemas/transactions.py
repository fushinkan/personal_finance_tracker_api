from pydantic import BaseModel, Field, field_validator
from sqlalchemy.ext.asyncio import AsyncSession

from features.transaction_enum import TransactionType

from datetime import datetime
from typing import TypeVar

T = TypeVar("T")


class TransactionsSchema(BaseModel):
    amount: float = Field(gt=0, description="The transaction amount must be greater than 0")
    category: str = Field(max_length=32, description="Transaction category")
    date: datetime | None = Field(None, description="Transaction datetime (default is current)")
    description: str | None = Field(max_length=512, description="Transaction description")
    transaction_type: TransactionType = Field(..., description="Transaction type: income or expense")

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        return round(amount, 2)


class TransactionsDisplaySchema(BaseModel):
    page: int = Field(1, description="current page")
    per_page: int = Field(10, description="number of records per page")
    sort_by: str | None = Field("created_at", description="column for sorting")
    sort_order: str | None = Field("desc", description="sort order")
    start_date: datetime | None = Field(None, description="start date for sorting")
    end_date: datetime | None = Field(None, description="end date for sorting")
    category: str | None = Field(None, description="transaction category")
    transaction_type: TransactionType | None = Field(None, description="transaction_type")
