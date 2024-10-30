from src.services.services import get_message


async def test_get_message(btc_message_json: str, eth_message_json: str):
    result = get_message(ticker="btc_usd")
    assert result == btc_message_json

    result = get_message(ticker="eth_usd")
    assert result == eth_message_json
