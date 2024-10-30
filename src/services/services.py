import json
import logging
from typing import Any

import websockets
from sqlalchemy.exc import DatabaseError, OperationalError

from src.config import LOGGING_FORMAT, LOGGING_LEVEL, WEBSOCKET_URL, Currencies
from src.database import get_db_session
from src.models.models import PriceIndex

logger = logging.getLogger(__name__)


def setup_logging():
    """
    Насройка логов.
    """
    logging.basicConfig(level=LOGGING_LEVEL, format=LOGGING_FORMAT)

    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.setLevel(LOGGING_LEVEL)


async def get_currencies():
    """
    Асинхронная функция-генератор поставляющая тикеры валют.
    """
    for currency in Currencies:
        yield currency.value


def get_message(ticker):
    """
    Создаем запрос для получения index price.
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
        logging.error("Error in database", exc_info=True)


async def get_price_index(ticker: str) -> dict[str, Any]:
    """
    Кидаем запрос в сокет и тянем ответ.
    """

    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            await websocket.send(get_message(ticker))
            while websocket.open:
                response = await websocket.recv()
                return json.loads(response)
    except (websockets.WebSocketException, websockets.InvalidStatusCode) as e:
        logger.error("Websocket error", exc_info=True)
