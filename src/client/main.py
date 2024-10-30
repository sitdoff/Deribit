import asyncio

from src.database import create_db
from src.services.services import get_currencies, get_price_index, save_data


async def main():
    while True:
        async for currency in get_currencies():
            data = await get_price_index(currency)
            await save_data(data=data, ticker=currency)
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(create_db())
    asyncio.run(main())
