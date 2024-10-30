from datetime import date, datetime, timedelta

from fastapi import HTTPException, status

from src.config import MICROSECONDS_IN_SECOND


def parse_date(target_date: str) -> date:
    """
    Получаем объект date из строки.
    """
    try:
        parsed_date = datetime.strptime(target_date, "%d.%m.%Y").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный формат даты. Дата должна быть в формате DD.MM.YYYY ",
        )
    return parsed_date


def get_timestamp_range(date: str) -> tuple[int, int]:
    """
    Получаем время начала и конца переданной даты.
    """
    date = parse_date(date)
    start = int(datetime.combine(date, datetime.min.time()).timestamp() * MICROSECONDS_IN_SECOND)
    end = int((datetime.combine(date, datetime.min.time()) + timedelta(days=1)).timestamp() * MICROSECONDS_IN_SECOND)
    return start, end
