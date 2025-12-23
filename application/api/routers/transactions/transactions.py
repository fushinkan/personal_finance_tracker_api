from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from application.api.dependencies.get_user import get_current_user
from application.api.dependencies.transactions import get_transactions_params
from application.api.handlers.transactions import TransactionsService
from application.database.models.users import Users
from application.schemas.transactions import (
    TransactionsSchema, 
    PagedTransactionsDisplaySchema,
    TransactionResponseWithMetaSchema,
    DeleteResponseSchema,
    TransactionsResponseSchema
)

from application.database.base import get_session
from application.schemas.transactions import TransactionResponseWithMetaSchema


from typing import Dict, Any


router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/new", status_code=status.HTTP_201_CREATED)
async def new_transaction_endpoint(
    transaction_data: TransactionsSchema,
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> TransactionsResponseSchema:
    """
    Creating a new transactions for concrete user.
    
    A JWT Token is required

    Args:
        user_data: transaction data
        current_user: concrete user from dependency
        session: AsyncSession from settings 
    
    Returns:
        The result of the service layer's work
    """

    try:
        result = await TransactionsService.create_transaction_handler(
            user_id=current_user.id,
            amount=transaction_data.amount,
            category=transaction_data.category,
            transaction_type=transaction_data.transaction_type,
            description=transaction_data.description,
            session=session
        )

        return result

    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal service error: {str(e)}"
        )

@router.get("/paged_transactions", status_code=status.HTTP_200_OK, response_model=TransactionResponseWithMetaSchema)
async def paged_transactions_endpoint(
    transaction_data: PagedTransactionsDisplaySchema = Depends(get_transactions_params),
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> TransactionResponseWithMetaSchema:
    #Doc string

    try:
        result = await TransactionsService.paged_transactions_handler(
            user_id=current_user.id,
            category=transaction_data.category,
            transaction_type=transaction_data.transaction_type,
            start_date=transaction_data.start_date,
            end_date=transaction_data.end_date,
            page=transaction_data.page,
            per_page=transaction_data.per_page,
            sort_by=transaction_data.sort_by,
            sort_order=transaction_data.sort_order,
            session=session
        )

        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal service error: {str(e)}"
        )

@router.get("/{transaction_id}", status_code=status.HTTP_200_OK, response_model=TransactionResponseWithMetaSchema)
async def get_concrete_transaction_endpoint(
    transaction_id: int = Path(..., description="transaction_id", ge=1),
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> TransactionResponseWithMetaSchema:
    #Doc String

    try:
        result = await TransactionsService.get_concrete_transaction_handler(
            user_id=current_user.id,
            transaction_id=transaction_id,
            session=session
        )

        return result
     
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal service error: {str(e)}"
        )

@router.delete("/{transaction_id}", status_code=status.HTTP_200_OK, response_model=DeleteResponseSchema)
async def delete_concrete_transaction_endpoint(
    transaction_id: int = Path(..., description="transaction_id", ge=1),
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> DeleteResponseSchema:
    #Doc String

    try:
        result = await TransactionsService.delete_concrete_transaction_handler(
            transaction_id=transaction_id,
            user_id=current_user.id,
            session=session
        )

        return result
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal service error"
        )