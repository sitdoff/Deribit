from pydantic import BaseModel


class PriceIndexPydantic(BaseModel):
    """
    Модель для ответов FastAPI.
    """

    ticker: str
    index_price: float
    timestamp: int
