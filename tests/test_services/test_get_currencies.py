from src.config import Currencies
from src.services.services import get_currencies


def test_get_currencies():
    result = []
    for currency in get_currencies():
        result.append(currency)

    assert result == [currency.value for currency in Currencies]
