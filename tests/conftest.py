import json

import pytest


@pytest.fixture
def btc_message_json():
    msg = {
        "jsonrpc": "2.0",
        "method": "public/get_index_price",
        "params": {
            "index_name": "btc_usd",
        },
    }
    return json.dumps(msg)


@pytest.fixture
def eth_message_json():
    msg = {
        "jsonrpc": "2.0",
        "method": "public/get_index_price",
        "params": {
            "index_name": "eth_usd",
        },
    }
    return json.dumps(msg)
