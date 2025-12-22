from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete

from application.database.models.users import Users
from application.database.models.tokens import Tokens
from application.api.dependencies.get_user import get_current_user
from application.database.base import get_session

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user_endpoint(
    current_user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Logout for concrete user.
    """

    try:
        await session.execute(
            delete(Tokens)
            .where(Tokens.user_id == current_user.id)
        )

        await session.commit()

        return {"message": "Successfully logged out"}
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed due to database error"
        )

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )