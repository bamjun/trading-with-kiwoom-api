from datetime import datetime
from typing import Any, Dict

import httpx
from django.conf import settings


class StockService:
    def __init__(self) -> None:
        # 실제 구현에서는 여기에 API 키나 기본 URL 등을 설정할 수 있습니다
        self.base_url = getattr(
            settings, "STOCK_API_BASE_URL", "https://your-stock-api-provider.com/api"
        )
        self.api_key = getattr(
            settings, "STOCK_API_KEY", "YOUR_API_KEY"
        )  # 실제 API 키로 교체해야 합니다
        # httpx 클라이언트 생성
        self.client = httpx.Client(
            timeout=10.0, headers={"Authorization": f"Bearer {self.api_key}"}
        )

    def get_stock_price(self, stock_code: str) -> Dict[str, Any]:
        """
        주어진 종목코드에 대한 시세 정보를 가져옵니다.
        """
        try:
            # requests 대신 httpx 사용
            response = self.client.get(
                f"{self.base_url}/stocks/{stock_code}",
            )
            response.raise_for_status()
            data = response.json()

            # 받아온 데이터를 원하는 형식으로 변환
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
            # 오류 처리
            raise Exception(f"주식 시세 조회 중 오류 발생: {str(e)}")

    def __del__(self) -> None:
        """
        서비스 객체가 소멸될 때 클라이언트를 닫습니다.
        """
        if hasattr(self, "client"):
            self.client.close()
