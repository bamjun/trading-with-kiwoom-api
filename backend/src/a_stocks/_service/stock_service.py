from datetime import datetime
from typing import Any, Dict

from a_stocks._utils.kiwoom_api import KiwoomAPI


class StockService:
    def __init__(self) -> None:
        self.api = KiwoomAPI()

    def get_stock_price(self, stock_code: str) -> Dict[str, Any]:
        """
        주어진 종목코드에 대한 시세 정보를 가져옵니다.
        """
        try:
            data = self.api.get_stock_price(stock_code)

            return {
                "code": stock_code,
                "name": data.get("name"),
                "current_price": data.get("price"),
                "previous_close": data.get("prev_close"),
                "change": data.get("price_change"),
                "change_percent": data.get("price_change_percent"),
                "volume": data.get("volume"),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        except Exception as e:
            raise Exception(f"주식 시세 조회 중 오류 발생: {str(e)}")

    def __del__(self) -> None:
        """
        서비스 객체가 소멸될 때 클라이언트를 닫습니다.
        """
        if hasattr(self, "client"):
            self.client.close()
