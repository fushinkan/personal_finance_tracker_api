from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from fastapi import HTTPException, status

from application.database.models.users import Users
from application.database.models.transactions import Transactions
from features.transaction_enum import TransactionType

from datetime import datetime, timezone
from typing import Dict, Any

class Transactions:
    #Method for adding a transaction
    @classmethod
    async def create_transaction_handler(
        user_id: int,
        amount: float,
        category: str,
        session: AsyncSession,
        transaction_type: TransactionType,
        date: datetime | None = None,
        description: str | None = None,
    ) -> Dict[str, Any]:
        """
        Docstring for new_transaction_handler

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
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service temporarily unavailable"
            )
        
        transaction_date = date or datetime.now(tz=timezone.utc)

        try:

            new_transaction = Transactions(
                user_id=user_id,
                amount=amount,
                category=category,
                description=description,
                transaction_type=transaction_type,
                created_at=transaction_date
            )

            session.add(new_transaction)
            await session.commit()
            await session.refresh(new_transaction)

            return {
                "message": "Transaction created successfully",
                "transaction_id": new_transaction.id,
                "user_id": new_transaction.user_id,
                "amount": new_transaction.amount,
                "category": new_transaction.category,
                "transaction_type": new_transaction.transaction_type.value,
                "description": new_transaction.description,
                "created_at": new_transaction.created_at.isoformat() if new_transaction.created_at else None
            }

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service temporarily unavailable"
            )

    #Method for displaying all transactions
    #Method for displaying transaction with pagination
    #Method for displaying concrete transaction
    #Method for deleting concrete transaction