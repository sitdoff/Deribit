import asyncio
import logging
from unittest.mock import AsyncMock, patch

import websockets

from src.services.services import handle_ticker

TICKER = "btc_usd"

TEST_WAITING_TIME = 0.1

data = {
    "result": {"index_price": 100},
    "usOut": 123,
}


@patch("src.services.services.WAITING_TIME_SECONDS", new=TEST_WAITING_TIME)
@patch("src.services.services.save_data")
@patch("src.services.services.get_price_index")
async def test_handle_ticker_success(mocked_get_price_index, mocked_save_data):

    mocked_get_price_index.return_value = data

    mocked_websocket = AsyncMock(name="Mocked websocket")
    mocked_websocket.open = True

    mocked_connection = AsyncMock(name="Mocked connection")
    mocked_connection.__aenter__.return_value = mocked_websocket

    with patch("src.services.services.websockets.connect", return_value=mocked_connection):

        async def close_websocker_after_first_iteration():
            mocked_websocket.open = False

        asyncio.create_task(close_websocker_after_first_iteration())
        await handle_ticker(TICKER)

    mocked_get_price_index.assert_called_once_with(TICKER, mocked_websocket)
    mocked_save_data.assert_called_once_with(data=data, ticker=TICKER)


@patch("src.services.services.WAITING_TIME_SECONDS", new=TEST_WAITING_TIME)
@patch("src.services.services.save_data")
@patch("src.services.services.get_price_index")
async def test_handle_ticker_data_is_none(mocked_get_price_index, mocked_save_data, caplog):

    mocked_get_price_index.return_value = None

    mocked_websocket = AsyncMock(name="Mocked websocket")
    mocked_websocket.open = True

    mocked_connection = AsyncMock(name="Mocked connection")
    mocked_connection.__aenter__.return_value = mocked_websocket

    with patch("src.services.services.websockets.connect", return_value=mocked_connection):
        with caplog.at_level(logging.WARNING):

            async def close_websocker_after_first_iteration():
                mocked_websocket.open = False

            asyncio.create_task(close_websocker_after_first_iteration())
            await handle_ticker(TICKER)

    assert "Data is None\n" in caplog.text
    mocked_get_price_index.assert_called_once_with(TICKER, mocked_websocket)
    mocked_save_data.assert_not_called()


@patch("src.services.services.WAITING_TIME_SECONDS", new=TEST_WAITING_TIME)
@patch("src.services.services.save_data")
@patch("src.services.services.get_price_index")
async def test_handle_ticker_websocket_error(mocked_get_price_index, mocked_save_data, caplog):

    mocked_get_price_index.return_value = None

    mocked_websocket = AsyncMock(name="Mocked websocket")
    mocked_websocket.open = True

    mocked_connection = AsyncMock(name="Mocked connection")
    mocked_connection.__aenter__.side_effect = websockets.WebSocketException("Connection error")

    with patch("src.services.services.websockets.connect", return_value=mocked_connection):
        with caplog.at_level(logging.ERROR):
            await handle_ticker(TICKER)

    assert "Connection error" in caplog.text
    mocked_get_price_index.assert_not_called()
    mocked_save_data.assert_not_called()
