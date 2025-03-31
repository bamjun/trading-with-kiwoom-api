from datetime import datetime
from typing import Any, Dict, Optional, Union

import httpx
from django.conf import settings


class KiwoomAPI:
    def __init__(self) -> None:
        self.base_url = getattr(
            settings, "KIWOOM_API_BASE_URL", "https://api.kiwoom.com"
        )
        self.app_key = getattr(settings, "KIWOOM_APP_KEY")
        self.secret_key = getattr(settings, "KIWOOM_SECRET_KEY")
        self.access_token: Optional[str] = None
        self.token_expires_dt: Optional[datetime] = None
        self.client = httpx.Client(
            timeout=10.0, headers={"Content-Type": "application/json;charset=UTF-8"}
        )

    def _get_access_token(self) -> str:
        """
        OAuth 접근 토큰을 발급받습니다.
        """
        if (
            self.access_token
            and self.token_expires_dt
            and datetime.now() < self.token_expires_dt
        ):
            return self.access_token

        url = f"{self.base_url}/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "secretkey": self.secret_key,
        }

        response = self.client.post(url, json=data)
        response.raise_for_status()
        result = response.json()

        if result.get("return_code") != 0:
            raise Exception(f"토큰 발급 실패: {result.get('return_msg')}")

        token = result.get("token")
        if not token:
            raise Exception("토큰이 없습니다.")

        self.access_token = token
        self.token_expires_dt = datetime.strptime(result["expires_dt"], "%Y%m%d%H%M%S")

        if self.access_token is None:
            raise Exception("토큰이 없습니다.")

        return self.access_token

    def _make_request(
        self, method: str, endpoint: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """
        API 요청을 보내고 응답을 처리합니다.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self._get_access_token()}"}

        response = self.client.request(
            method=method, url=url, headers=headers, **kwargs
        )
        response.raise_for_status()
        result: Dict[str, Any] = response.json()

        if result.get("return_code") != 0:
            raise Exception(f"API 요청 실패: {result.get('return_msg')}")

        return result

    def get_stock_price(self, stock_code: str) -> Dict[str, Any]:
        """
        주식 시세 정보를 조회합니다.
        """
        return self._make_request("GET", f"/v1/stock/price/{stock_code}")

    def get_stock_info(self, stock_code: str) -> Dict[str, Any]:
        """
        종목 기본 정보를 조회합니다.
        """
        return self._make_request("GET", f"/v1/stock/info/{stock_code}")

    def get_account_balance(self) -> Dict[str, Any]:
        """
        계좌 잔고를 조회합니다.
        """
        return self._make_request("GET", "/v1/account/balance")

    def get_order_history(self, account_number: str) -> Dict[str, Any]:
        """
        주문 내역을 조회합니다.
        """
        return self._make_request("GET", f"/v1/order/history/{account_number}")

    def __del__(self) -> None:
        """
        클라이언트 연결을 종료합니다.
        """
        if hasattr(self, "client"):
            self.client.close()
