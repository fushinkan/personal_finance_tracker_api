from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from application.database.models.users import Users
from application.database.models.tokens import Tokens
from application.core.password import Password
from application.core.jwt_generation import JWTGeneration

from typing import Dict
from datetime import datetime, timezone, timedelta

class User:

    # Method for Adding a user
    @classmethod
    async def register_users_handler(
        cls,
        *, 
        username: str, 
        email: str, 
        password: str, 
        session: AsyncSession
    ) -> Dict[str, str]:
        #Doc String

        # Password hashing
        hashed_password = Password.hashed_psw(password=password)

        #Adding User to DB
        new_user = Users(
            username=username,
            email=email,
            hashed_password=hashed_password
        )

        session.add(new_user)
        await session.commit()

        return {"message": "The User has been successfully registered"}

    #Method for Logging a user
    @classmethod
    async def login_user_handler(
        cls,
        *,
        email: str,
        password: str,
        session: AsyncSession
    ) -> Dict[str, str]: 
        #Doc String
        
        result = await session.execute(
            select(Users)
            .where(Users.email == email)
        )
        
        existing_user = result.scalar_one_or_none()

        if existing_user and Password.verify_password(plain_password=password, hashed_password=existing_user.hashed_password):
            refresh_payload = {
                "sub": str(existing_user.id),
                "exp": datetime.now(tz=timezone.utc) + timedelta(days=30)
            }

            refresh_token = Tokens(
                token=JWTGeneration.encode_jwt(payload=refresh_payload)
            )

            existing_user.token = refresh_token
            
            session.add(refresh_token)
            await session.commit()


    # Method for Updating a user
    # Method for Deleting a user
    # Method for Displaying a user