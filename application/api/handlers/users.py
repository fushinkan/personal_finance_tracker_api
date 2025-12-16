from sqlalchemy.ext.asyncio import AsyncSession

from application.database.models.users import Users

class Users:

    # Method for Adding a user
    async def register_users_handler(*, username: str, email: str, hashed_password: str, session: AsyncSession):
        
        new_user = Users(
            username=username,
            email=email,
            hashed_password=hashed_password
        )

        session.add(new_user)
        await session.commit()

    # Method for Updating a user
    # Method for Deleting a user
    # Method for Displaying a user