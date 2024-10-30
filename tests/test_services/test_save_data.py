import logging
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, patch

from sqlalchemy.exc import DatabaseError, OperationalError

from src.services.services import save_data

TICKER = "btc_usd"
data = {
    "result": {"index_price": 100},
    "usOut": 123,
}


async def test_save_data_success():
    mock_session = AsyncMock()

    @asynccontextmanager
    async def mocked_get_db_session():
        yield mock_session

    with patch("src.services.services.get_db_session", new=mocked_get_db_session):
        await save_data(data=data, ticker=TICKER)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


async def test_save_data_operational_error(caplog):
    mock_session = AsyncMock()
    statement = "INSERT INTO price_index (ticker, index_price, timestamp) VALUES (?, ?, ?)"
    params = (TICKER, data["result"]["index_price"], data["usOut"])
    orig = Exception("Mocked operational error")
    mock_session.commit.side_effect = OperationalError(statement, params, orig)

    @asynccontextmanager
    async def mocked_get_db_session():
        yield mock_session

    with patch("src.services.services.get_db_session", new=mocked_get_db_session):
        with caplog.at_level(logging.ERROR):
            await save_data(data, TICKER)

            assert "Error in database" in caplog.text
            assert "Mocked operational error" in caplog.text
        mock_session.commit.assert_called_once()


async def test_save_data_database_error(caplog):
    mock_session = AsyncMock()
    statement = "INSERT INTO price_index (ticker, index_price, timestamp) VALUES (?, ?, ?)"
    params = (TICKER, data["result"]["index_price"], data["usOut"])
    orig = Exception("Mocked database error")
    mock_session.commit.side_effect = DatabaseError(statement, params, orig)

    @asynccontextmanager
    async def mocked_get_db_session():
        yield mock_session

    with patch("src.services.services.get_db_session", new=mocked_get_db_session):
        with caplog.at_level(logging.ERROR):
            await save_data(data, TICKER)

            assert "Error in database" in caplog.text
            assert "Mocked database error" in caplog.text
