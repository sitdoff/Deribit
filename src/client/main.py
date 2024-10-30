import asyncio
import logging

from src.database import create_db
from src.services.services import (
    get_currencies,
    get_price_index,
    save_data,
    setup_logging,
)

logger = logging.getLogger(__name__)


async def main():
    while True:
        async for currency in get_currencies():
            data = await get_price_index(currency)
            if not data is None:
                await save_data(data=data, ticker=currency)
            else:
                logger.warning("Data is None")

        await asyncio.sleep(60)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(create_db())
    asyncio.run(main())
