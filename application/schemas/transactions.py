from pydantic import BaseModel, Field, ConfigDict

from features.transaction_enum import TransactionType
from application.schemas.users import UserResponseSchema

from datetime import datetime
from typing import TypeVar

T = TypeVar("T")


class TransactionsSchema(BaseModel):
    amount: float = Field(gt=0, description="The transaction amount must be greater than 0")
    category: str = Field(max_length=32, description="Transaction category")
    description: str | None = Field(max_length=512, description="Transaction description")
    transaction_type: TransactionType = Field(..., description="Transaction type: income or expense")


class PagedTransactionsDisplaySchema(BaseModel):
    page: int = Field(1, description="current page")
    per_page: int = Field(10, description="number of records per page")
    sort_by: str | None = Field("created_at", description="column for sorting")
    sort_order: str | None = Field("desc", description="sort order")
    start_date: datetime | None = Field(None, description="start date for sorting")
    end_date: datetime | None = Field(None, description="end date for sorting")
    category: str | None = Field(None, description="transaction category")
    transaction_type: TransactionType | None = Field(None, description="transaction_type")

class TransactionsResponseSchema(TransactionsSchema):
    id: int = Field(..., ge=1)
    created_at: datetime = Field(...)
    user: UserResponseSchema | None = None

    model_config = ConfigDict(from_attributes=True)

class TransactionResponseWithMetaSchema(BaseModel):
    data: list[TransactionsResponseSchema]
    meta: dict
    
    model_config = ConfigDict(from_attributes=True)

class DeleteResponseSchema(BaseModel):
    message: str = Field(...)
    deleted_id: int = Field(..., ge=1)
    deleted_at: datetime = Field(...)