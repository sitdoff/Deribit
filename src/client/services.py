import json
import logging
from typing import Any

import websockets
from sqlalchemy.exc import DatabaseError, OperationalError

from ..config import Currencies
from ..database import get_db_session
from ..models.models import PriceIndex

logger = logging.getLogger(__name__)


async def get_currencies():
    """
    Асинхронная функция-генератор поставляющая тикеры валют.
    """
    for currency in Currencies:
        yield currency.value


def get_message(ticker):
    """
    Создаем RPC запрос для получения index price.
    """

    msg = {
        "jsonrpc": "2.0",
        "method": "public/get_index_price",
        "params": {
            "index_name": f"{ticker}",
        },
    }
    return json.dumps(msg)


async def save_data(data, ticker):
    """
    Сохраняем данные в базу.
    """

    try:
        async with get_db_session() as session:
            price_index = PriceIndex(
                ticker=ticker,
                index_price=data["result"]["index_price"],
                timestamp=data["usOut"],
            )
            session.add(price_index)
            await session.commit()
    except (OperationalError, DatabaseError) as exc:
        logging.error("Error in database", exc)


async def get_price_index(ticker: str) -> dict[str, Any]:
    """
    Кидаем запрос в сокет и тянем ответ.
    """

    try:
        async with websockets.connect("wss://test.deribit.com/ws/api/v2") as websocket:
            await websocket.send(get_message(ticker))
            while websocket.open:
                response = await websocket.recv()
                return json.loads(response)
    except websockets.WebSocketException as e:
        logger.error("Websocket error", e)
