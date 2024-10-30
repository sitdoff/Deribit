import json
import logging
from unittest.mock import AsyncMock, patch

from websockets import WebSocketException

from src.services.services import get_price_index

TICKER = "btc_usd"
data = {
    "result": {"index_price": 100},
    "usOut": 123,
}


async def test_get_price_index_success():
    with patch("src.services.services.get_message", return_value="success message"):
        mocked_connect = AsyncMock()
        mocked_websocket = AsyncMock()
        mocked_websocket.recv.return_value = json.dumps(data)
        mocked_connect.__aenter__.return_value = mocked_websocket

        with patch("websockets.connect", return_value=mocked_connect):
            result = await get_price_index(TICKER)

            mocked_websocket.send.assert_called_once_with("success message")
            assert result == data


async def test_get_price_index_websocket_error(caplog):
    with patch("websockets.connect", side_effect=WebSocketException("Connection error", "params", "orig")):
        with caplog.at_level(logging.ERROR):
            result = await get_price_index(TICKER)

            assert result is None

            assert "Websocket error" in caplog.text
            assert "Connection error" in caplog.text
