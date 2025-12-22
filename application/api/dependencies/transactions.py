from fastapi import Query

from application.schemas.transactions import TransactionsDisplaySchema
from features.transaction_enum import TransactionType

from datetime import datetime

def get_transactions_params(
    page: int = Query(1, description="current page"),
    per_page: int = Query(10, description="number of records per page"),
    sort_by: str | None = Query("created_at", description="column for sorting"),
    sort_order: str | None = Query("desc", description="sort order"),
    start_date: datetime | None = Query(None, description="start date for sorting"),
    end_date: datetime | None = Query(None, description="end date for sorting"),
    category: str | None = Query(None, description="transaction category"),
    transaction_type: TransactionType | None = Query(None, description="transaction_type")
) -> TransactionsDisplaySchema:
    #Doc string

    return TransactionsDisplaySchema(
        page=page,
        per_page=per_page,
        sort_by=sort_by,
        sort_order=sort_order,
        start_date=start_date,
        end_date=end_date,
        category=category,
        transaction_type=transaction_type
    )