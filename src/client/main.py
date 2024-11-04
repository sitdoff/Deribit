import asyncio
import logging

from src.database import create_db
from src.services.services import get_currencies, handle_ticker, setup_logging

logger = logging.getLogger(__name__)


async def main():
    tasks = [handle_ticker(currency) for currency in get_currencies()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(create_db())
    asyncio.run(main())
