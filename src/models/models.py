from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PriceIndex(Base):
    """
    SQLAlchemy модель для записи данных в базу.
    """

    __tablename__ = "price_index"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(10))
    index_price: Mapped[Decimal] = mapped_column(Numeric(precision=8, scale=2))
    timestamp: Mapped[int] = mapped_column()
