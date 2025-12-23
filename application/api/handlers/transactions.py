from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, desc, asc, and_, func, delete
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from application.database.models.users import Users
from application.database.models.transactions import Transactions
from features.pagination_enum import SortOrder, SortField
from features.transaction_enum import TransactionType
from application.schemas.transactions import (
    TransactionResponseWithMetaSchema, 
    DeleteResponseSchema, 
    TransactionsResponseSchema
)

from datetime import datetime, timezone
from typing import Dict, Any

class TransactionsService:
    #Method for adding a transaction
    @classmethod
    async def create_transaction_handler(
        cls,
        *,
        user_id: int,
        amount: float,
        category: str,
        session: AsyncSession,
        transaction_type: TransactionType,
        description: str | None = None,
    ) -> TransactionsResponseSchema:
        """
        Creating new transaction for concrete user.

        Args:
            user_id: user ID from DB
            amount: transaction amount
            category: transaction category
            transaction_type: transaction type: income or expense
            description: transaction description
            session: AsyncSession

        Returns:
            

        Raises:
            HTTPException 400: If amount less or equal than 0
            HTTPException 404: If user not found
            HTTPException 503: In case of database errors
        """

        if amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount must be greater than 0"
            )
    
        if not isinstance(transaction_type, TransactionType):
            valid_types = [t.value for t in TransactionType]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid transaction type. Must be one of: {valid_types}"
            )

        try:
            result = await session.execute(
                select(Users)
                .where(Users.id == user_id)
            )

            existing_user = result.scalar_one_or_none()

            if not existing_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service temporarily unavailable"
            )
        
        transaction_date = datetime.now(tz=timezone.utc)

        try:

            new_transaction = Transactions(
                user_id=user_id,
                amount=amount,
                category=category.strip().title(),
                description=description.strip() if description else "",
                transaction_type=transaction_type,
                created_at=transaction_date
            )

            session.add(new_transaction)
            await session.commit()
            await session.refresh(new_transaction)

            return TransactionsResponseSchema.model_validate(new_transaction, from_attributes=True)

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service temporarily unavailable"
            )

    #Method for displaying all transactions
    @classmethod
    async def paged_transactions_handler(
        cls, 
        *,
        session: AsyncSession,
        user_id: int,
        page: int = 1,
        per_page: int = 10,
        category: str | None = None,
        transaction_type: TransactionType | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> TransactionResponseWithMetaSchema:
        #Doc string

        offset = (page - 1) * per_page

        query = (
            select(Transactions)
            .where(Transactions.user_id == user_id)
            .options(
                selectinload(Transactions.user)
            )
        )

        if category:
            query = query.where(Transactions.category == category)

        transaction_type_value = None
        if transaction_type:
            if isinstance(transaction_type, TransactionType):
                transaction_type_value = transaction_type.value
            else:
                try:
                    transaction_type_enum = TransactionType(transaction_type)
                    transaction_type_value = transaction_type_enum.value
                except (ValueError, AttributeError):
                    transaction_type_value = transaction_type
            if transaction_type_value:
                query = query.where(Transactions.transaction_type == transaction_type_value)

        date_filters = []

        if start_date:

            date_filters.append(Transactions.created_at >= start_date)

        if end_date:
            end_date_with_time = end_date.replace(hour=23, minute=59, second=59)
            date_filters.append(Transactions.created_at <= end_date_with_time)

        if date_filters:
            query = query.where(and_(*date_filters))

        sort_mapping = {
            SortField.CREATED_AT.value: Transactions.created_at,
            SortField.AMOUNT.value: Transactions.amount,
            SortField.DATE.value: Transactions.created_at,
            SortField.UPDATED_AT.value: Transactions.updated_at,
            SortField.CATEGORY.value: Transactions.category,
            SortField.TRANSACTION_TYPE.value: Transactions.transaction_type
        }

        sort_field = sort_mapping.get(sort_by, Transactions.created_at)

        if sort_order.lower() == SortOrder.ASC.value:
            query = query.order_by(asc(sort_field))
        else:
            query = query.order_by(desc(sort_field))

        total_records_query = query.with_only_columns(func.count()).order_by(None)

        total_records_result = await session.execute(total_records_query)
        total_records = total_records_result.scalar_one()

        paginated_query = query.offset(offset).limit(per_page)

        result = await session.execute(paginated_query)
        transactions = result.scalars().all()

        transaction_data = [
            TransactionsResponseSchema.model_validate(t, from_attributes=True) for t in transactions
            ]

        total_pages = (total_records + per_page - 1) // per_page if total_records > 0 else 1

        return TransactionResponseWithMetaSchema(
            data=transaction_data,
            meta={
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total_records": total_records,
                    "total_pages": total_pages,
                    "has_next": page < total_pages,
                    "has_prev": page > 1
                },
                "filters": {
                    "category": category,
                    "transaction_type": transaction_type_value,
                    "start_date": start_date.isoformat() if start_date else None,
                    "end_date": end_date.isoformat() if end_date else None
                },
                "sort": {
                    "by": sort_by,
                    "order": sort_order
                }
            }
        )
    
    #Method for displaying concrete transaction
    @classmethod
    async def get_concrete_transaction_handler(
        cls, 
        *,
        user_id: int,
        transaction_id: int, 
        session: AsyncSession
    ) -> TransactionResponseWithMetaSchema:
        #Doc string

        try:
            result = await session.execute(
                select(Transactions)
                .where(
                    and_(
                        Transactions.id == transaction_id,
                        Transactions.user_id == user_id
                    )
                )
                .options(
                    selectinload(Transactions.user)
                )
            )

            transaction = result.scalar_one_or_none()

            if not transaction:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="transaction not found"
                )
            
            transaction_data = TransactionsResponseSchema.model_validate(transaction, from_attributes=True)

            return TransactionResponseWithMetaSchema(
                data=[transaction_data],
                meta={
                    "user_id": user_id,
                    "transaction_id": transaction.id,
                    "retrieved_at": datetime.now(tz=timezone.utc).isoformat()
                }
            )
        
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service temporarily unavailable"
            )
        
    #Method for deleting concrete transaction
    @classmethod
    async def delete_concrete_transaction_handler(
        cls, 
        *,
        user_id: int, 
        transaction_id: int,
        session: AsyncSession
    ) -> DeleteResponseSchema:
        #Doc String

        try:
            check = await session.execute(
                select(Transactions)
                .where(
                    and_(
                        Transactions.id == transaction_id,
                        Transactions.user_id == user_id
                    )
                )
            )

            transaction = check.scalar_one_or_none()

            if not transaction:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="transaction not found"
                )

            await session.execute(
                delete(Transactions)
                .where(
                    and_(
                        Transactions.id == transaction_id,
                        Transactions.user_id == user_id
                    )
                )
            )

            await session.commit()

            return DeleteResponseSchema(
                message=f"Transaction {transaction_id} was successfully deleted",
                deleted_id=transaction_id,
                deleted_at=datetime.now(tz=timezone.utc)
            )

        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service temporarily unavailable"
            )

    #Method for displaying transaction with cursor-based pagination