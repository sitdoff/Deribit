from datetime import date, datetime, timedelta

from src.config import MICROSECONDS_IN_SECOND


def get_timestamp_range(date: date) -> tuple[int, int]:
    start = int(datetime.combine(date, datetime.min.time()).timestamp() * MICROSECONDS_IN_SECOND)
    end = int((datetime.combine(date, datetime.min.time()) + timedelta(days=1)).timestamp() * MICROSECONDS_IN_SECOND)
    return start, end
