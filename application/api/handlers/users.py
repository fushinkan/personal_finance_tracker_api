from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from application.database.models.users import Users
from application.database.models.tokens import Tokens
from application.core.password import Password
from application.core.jwt_generation import JWTGeneration

from typing import Dict
from datetime import datetime, timezone, timedelta

class UserService:

    # Method for adding a user
    @classmethod
    async def register_users_handler(
        cls,
        *, 
        username: str, 
        email: str, 
        password: str, 
        session: AsyncSession
    ) -> Dict[str, str]:
        """
        Registering a new user.
        
        Args:
            username: Username
            email: Email (unique constraint)
            password: Password (Will be hashed)
            session: AsyncSession 
        
        Returns:
            Dict with message of success and user_id

        Raises:
            HTTPException 400: If email has been registered
            HTTPException 503: In case with database errors
        """
        
        try:
            result = await session.execute(
                select(Users.id)
                .where(Users.email == email)
            )

            existing_email = result.scalar_one_or_none()

            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            # Password hashing
            hashed_password = Password.hashed_psw(password=password)

            #Adding User to DB
            new_user = Users(
                username=username,
                email=email.strip().lower(),
                hashed_password=hashed_password
            )

            session.add(new_user)
            await session.commit()

            return {
                "message": "The User has been successfully registered",
                "user_id": new_user.id
            }

        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service temporarily unavailable"
            )

    #Method for authorization a user
    @classmethod
    async def login_user_handler(
        cls,
        *,
        email: str,
        password: str,
        session: AsyncSession
    ) -> Dict[str, str]: 
        """
        Authorization for an existing user.
        
        Args:
            email: Email (unique constraint)
            password: Password (Will be hashed)
            session: AsyncSession 
        
        Returns:
            Dict with access_token, refresh_token and token_type

        Raises:
            HTTPException 401: If user entered incorrect credentials
            HTTPException 503: In case with database errors
        """
        
        try:
            result = await session.execute(
                select(Users)
                .where(Users.email == email.strip().lower())
            )
            
            existing_user = result.scalar_one_or_none()

            if not existing_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            is_valid_password = Password.verify_password(plain_password=password, hashed_password=existing_user.hashed_password)

            if not is_valid_password:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Email or Password"
                )

            else:
                refresh_payload = {
                    "sub": str(existing_user.id),
                    "exp": datetime.now(tz=timezone.utc) + timedelta(days=30),
                    "type": "refresh"
                }

                refresh_token = Tokens(
                    token=JWTGeneration.encode_jwt(payload=refresh_payload)
                )

                existing_user.token = refresh_token
                
                access_payload = {
                    "sub": str(existing_user.id),
                    "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=15),
                    "type": "access"
                }

                access_token = JWTGeneration.encode_jwt(payload=access_payload)

                session.add(refresh_token)
                await session.commit()

                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token.token,
                    "token_type": "bearer"
                }

        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service temporarily unavailable"
            )

    # Method for updating a user
    # Method for deleting a user
    # Method for displaying a user