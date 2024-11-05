import json
from unittest.mock import AsyncMock, patch

from src.services.services import get_price_index

TICKER = "btc_usd"
data = {
    "result": {"index_price": 100},
    "usOut": 123,
}


async def test_get_price_index_success():
    with patch("src.services.services.get_message", return_value="success message") as mocked_get_message:
        mocked_websocket = AsyncMock()
        mocked_websocket.recv.return_value = json.dumps(data)

        result = await get_price_index(TICKER, mocked_websocket)

        mocked_get_message.assert_called_once_with(TICKER)
        mocked_websocket.send.assert_called_once_with("success message")
        mocked_websocket.recv.assert_called_once()
        assert result == data
