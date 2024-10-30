from pydantic import BaseModel


class PriceIndexPydantic(BaseModel):
    ticker: str
    index_price: float
    timestamp: int
