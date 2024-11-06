from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.api.helpers.helpers import get_timestamp_range
from src.models.models import PriceIndex


async def get_price_indexes_all(session: AsyncSession, ticker: str) -> Sequence[PriceIndex]:
    query = select(PriceIndex).where(PriceIndex.ticker == ticker)
    result = await session.execute(query)
    return result.scalars().all()


async def get_price_indexes_latest(session: AsyncSession, ticker: str) -> PriceIndex | None:
    query = select(PriceIndex).where(PriceIndex.ticker == ticker).order_by(PriceIndex.timestamp.desc()).limit(1)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_price_indexes_by_date(session: AsyncSession, ticker: str, target_date: str) -> Sequence[PriceIndex]:
    start, end = get_timestamp_range(target_date)

    query = (
        select(PriceIndex)
        .where(PriceIndex.ticker == ticker)
        .where(PriceIndex.timestamp >= start)
        .where(PriceIndex.timestamp < end)
    )

    result = await session.execute(query)
    return result.scalars().all()
