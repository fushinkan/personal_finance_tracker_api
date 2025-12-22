from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from application.schemas.users import UserLoginSchema
from application.api.handlers.users import UserService
from application.database.base import get_session

from typing import Dict

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user_endpoint(
    user_data: UserLoginSchema, 
    session: AsyncSession = Depends(get_session)
) -> Dict[str, str]:
    """
    Authorization for an existing user.
    
    Args:
        user_data: User Data
        session: AsyncSession from settings 
    
    Returns:
        The result of the service layer's work
    """

    try:

        tokens = await UserService.login_user_handler(
            email=user_data.email,
            password=user_data.password,
            session=session
        )

        return tokens

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )