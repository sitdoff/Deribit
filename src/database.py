from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import DATABASE_URL
from src.models.models import Base

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_db():
    """
    Создание базы.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_db_session():
    """
    Асинхронная функция-генератор выступающая в роли асинхронного контекстного менеджера. Поставляет сессию для БД.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
