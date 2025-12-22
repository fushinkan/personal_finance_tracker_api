from pydantic import BaseModel, Field, field_validator

from features.pagination_enum import SortField, SortOrder
from application.schemas.transactions import TransactionsFilterSchema

from typing import TypeVar, Generic

T = TypeVar("T")

class PaginationParamsSchema(BaseModel):
    page: int = Field(1, ge=1, description="page number (starts from 1)")
    per_page: int = Field(10, ge=1, le=100, description="records quantity per page")
    sort_by: str = Field(SortField.CREATED_AT, description="sorting field")
    sort_order: str = Field(SortOrder.DESC, description="sorting direction")

    @field_validator("per_page")
    @classmethod
    def validate_per_page(cls, *, value: T) -> T:
        #Doc string
        if value > 100:
            raise ValueError("maximum per_page is 100")
        return value
    
    @classmethod
    def get_offset(cls) -> T:
        """Calculating offset for SQL request"""
        return (cls.page - 1) * cls.per_page

    @classmethod
    def get_limit(cls) -> T:
        """Getting the limit of the quantity of records per page"""
        return cls.per_page
    
class PaginatedResponse(BaseModel, Generic[T]):
    transaction: list[T]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
    filters: dict | None = None

    @classmethod
    def create(
        cls, 
        *,
        transactions: list[T],
        total: int,
        pagination: PaginationParamsSchema,
        filters: TransactionsFilterSchema | None = None
    ):
        
        total_pages = (total + pagination.per_page - 1) // pagination.per_page

        return cls(
            transactions=transactions,
            total=total,
            page=pagination.page,
            per_page=pagination.per_page,
            total_pages=total_pages,
            has_next=pagination.page < total_pages,
            has_prev=pagination.page > 1,
            filters=filters.model_dump() if filters else None
        )