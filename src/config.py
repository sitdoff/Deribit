import logging
from enum import Enum


class Currencies(Enum):
    """
    Здесь записываем тикеры валют, по которым надо получить данные.
    """

    BTC_USD = "btc_usd"
    ETH_USD = "eth_usd"


DATABASE_URL = "sqlite+aiosqlite:///./src/data/sqlite.db"
WEBSOCKET_URL = "wss://test.deribit.com/ws/api/v2"
WAITING_TIME_SECONDS = 60
MICROSECONDS_IN_SECOND = 1_000_000
SERVICE_NAME = "Client"
LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = f"{SERVICE_NAME} - %(asctime)s - %(levelname)s - %(message)s"
