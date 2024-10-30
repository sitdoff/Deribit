from contextlib import _AsyncGeneratorContextManager
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.api.helpers.helpers import get_timestamp_range
from src.api.models.price_index import PriceIndexPydantic
from src.database import get_db_session
from src.models.models import PriceIndex

router = APIRouter()


@router.get(
    "/index_prices/all",
    response_model=list[PriceIndexPydantic],
    status_code=status.HTTP_200_OK,
    tags=["price_index"],
    summary="Получение всех записей price_index.",
    description="Возвращает все сохраненные данные по указанной валюте.",
)
async def get_all_index_prices(
    ticker: Annotated[str, Query()],
    get_session: _AsyncGeneratorContextManager = Depends(get_db_session),
):
    async with get_session as session:
        price_indexes = await session.execute(select(PriceIndex).where(PriceIndex.ticker == ticker))
        price_indexes_list = price_indexes.scalars().all()

    if not price_indexes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price index not found")

    return price_indexes_list


@router.get(
    "/index_prices/latest",
    response_model=PriceIndexPydantic,
    status_code=status.HTTP_200_OK,
    tags=["price_index"],
    summary="Получение последней записи price_index.",
    description="Возвращает последнюю цену по указанной валюте.",
)
async def get_latest_index_price(
    ticker: Annotated[str, Query()],
    get_session: _AsyncGeneratorContextManager = Depends(get_db_session),
):
    async with get_session as session:
        result = await session.execute(
            select(PriceIndex).where(PriceIndex.ticker == ticker).order_by(PriceIndex.timestamp.desc()).limit(1)
        )
        price_index = result.scalar_one_or_none()

    if not price_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price index not found")

    return price_index


@router.get(
    "/index_prices/date",
    response_model=list[PriceIndexPydantic],
    status_code=status.HTTP_200_OK,
    tags=["price_index"],
    summary="Получение записей по дате.",
    description="Возвращает цену по указанной валюте с фильтром по дате.",
)
async def get_latest_index_price_by_date(
    ticker: Annotated[str, Query()],
    target_date: Annotated[date, Query(alias="date")],
    get_session: AsyncSession = Depends(get_db_session),
):
    start, end = get_timestamp_range(target_date)

    async with get_session as session:
        query = (
            select(PriceIndex)
            .where(PriceIndex.ticker == ticker)
            .where(PriceIndex.timestamp >= start)
            .where(PriceIndex.timestamp < end)
        )

        result = await session.execute(query)
        price_indexes_list = result.scalars().all()

    return price_indexes_list
