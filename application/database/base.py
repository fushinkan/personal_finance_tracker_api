from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from application.core.config import settings
from typing import AsyncGenerator


engine = create_async_engine(url=settings.get_session)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as connection:
        yield connection

class Base(DeclarativeBase):
    pass

