from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.schemas.users import UserCreateSchema
from application.api.handlers.users import Users
from application.database.base import get_session

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register_user_endpoint(*, user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    
    await Users.register_users_handler(
        email=user_data.email,
        hashed_password=user_data.hashed_password,
        username=user_data.username,
        session=session
    )

    return {"message": "User is Succesfully added"}