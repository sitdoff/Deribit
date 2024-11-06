from contextlib import _AsyncGeneratorContextManager
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_session
from src.schemas.price_index import PriceIndexPydantic
from src.services.api_services.price_index_services import (
    get_price_indexes_all,
    get_price_indexes_by_date,
    get_price_indexes_latest,
)

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
        result = await get_price_indexes_all(session, ticker)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price index not found")

    return result


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
        result = await get_price_indexes_latest(session, ticker)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price index not found")

    return result


@router.get(
    "/index_prices/date",
    response_model=list[PriceIndexPydantic],
    status_code=status.HTTP_200_OK,
    tags=["price_index"],
    summary="Получение записей по дате.",
    description="Возвращает цену по указанной валюте с фильтром по дате. Дата должна быть в формате DD.MM.YYYY .",
)
async def get_index_price_by_date(
    ticker: Annotated[str, Query()],
    target_date: Annotated[str, Query(regex=r"^\d{2}\.\d{2}\.\d{4}$", alias="date")],
    get_session: AsyncSession = Depends(get_db_session),
):

    async with get_session as session:
        result = await get_price_indexes_by_date(session, ticker, target_date)

    return result
