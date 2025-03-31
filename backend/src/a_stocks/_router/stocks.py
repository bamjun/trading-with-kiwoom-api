from typing import Any, Dict, Tuple, Union

from ninja import Router

from a_stocks._schema.stock_schema import ErrorOut, StockCodeIn, StockPriceOut
from a_stocks._service.stock_service import StockService

router = Router()
stock_service = StockService()


@router.get("/price/{stock_code}", response={200: StockPriceOut, 400: ErrorOut})
def get_stock_price(
    request: Any, stock_code: str
) -> Tuple[int, Union[Dict[str, Any], Dict[str, str]]]:
    """
    종목 코드를 받아 해당 주식의 현재 시세 정보를 반환합니다.
    """
    try:
        result = stock_service.get_stock_price(stock_code)
        return 200, result
    except Exception as e:
        return 400, {"message": str(e)}


@router.post("/price", response={200: StockPriceOut, 400: ErrorOut})
def get_stock_price_by_post(
    request: Any, data: StockCodeIn
) -> Tuple[int, Union[Dict[str, Any], Dict[str, str]]]:
    """
    POST 요청으로 종목 코드를 받아 해당 주식의 현재 시세 정보를 반환합니다.
    """
    try:
        result = stock_service.get_stock_price(data.code)
        return 200, result
    except Exception as e:
        return 400, {"message": str(e)}
