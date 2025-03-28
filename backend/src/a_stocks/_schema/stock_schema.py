from typing import Optional

from ninja import Schema


class StockCodeIn(Schema):
    code: str


class StockPriceOut(Schema):
    code: str
    name: Optional[str] = None
    current_price: float
    previous_close: float
    change: float
    change_percent: float
    volume: int
    timestamp: str


class ErrorOut(Schema):
    message: str
