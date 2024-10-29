from enum import Enum


class Currencies(Enum):
    """
    Здесь записываем тикеры валют, по которым надо получить данные.
    """

    BTC_USD = "btc_usd"
    ETH_USD = "eth_usd"


DATABASE_URL = "sqlite+aiosqlite:///./src/sqlite.db"
