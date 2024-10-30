from datetime import date, datetime, timedelta


def get_timestamp_range(date: date) -> tuple[int, int]:
    start = int(datetime.combine(date, datetime.min.time()).timestamp() * 1000000)
    end = int((datetime.combine(date, datetime.min.time()) + timedelta(days=1)).timestamp() * 1000000)
    return start, end
