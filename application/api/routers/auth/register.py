from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from application.schemas.users import UserCreateSchema
from application.api.handlers.users import UserService
from application.database.base import get_session

from typing import Dict

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user_endpoint(
    *, 
    user_data: UserCreateSchema, 
    session: AsyncSession = Depends(get_session)
)-> Dict[str, str]:
    """
    Registering a new user.
    
    Args:
        user_data: User Data
        session: AsyncSession from settings
    
    Returns:
        The result of the service layer's work
    """

    try:
        result = await UserService.register_users_handler(
            email=user_data.email,
            password=user_data.password,
            username=user_data.username,
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