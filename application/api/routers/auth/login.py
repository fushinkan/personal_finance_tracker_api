from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.schemas.users import UserLoginSchema
from application.api.handlers.users import User
from application.database.base import get_session

from typing import Dict

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login_user_endpoint(
    user_data: UserLoginSchema, 
    session: AsyncSession = Depends(get_session)
) -> Dict[str, str]:
    #Doc String

    await User.login_user_handler(
        email=user_data.email,
        password=user_data.password,
        session=session
    )

    return {"message": "The User has been successfully authorized"}