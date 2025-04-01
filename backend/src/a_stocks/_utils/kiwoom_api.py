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
        API ID: au10001
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

        assert self.access_token is not None
        return self.access_token

    def _make_request(
        self, method: str, api_id: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """
        API 요청을 보내고 응답을 처리합니다.
        
        Args:
            method (str): HTTP 메서드 (GET, POST)
            api_id (str): API ID
            **kwargs: API 요청에 필요한 추가 파라미터
        """
        url = f"{self.base_url}/api/dostk/acnt"
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json;charset=UTF-8",
            "api-id": api_id,
            "cont-yn": kwargs.get("cont_yn", "N"),
            "next-key": kwargs.get("next_key", "")
        }
        
        # API 요청 데이터 구성
        request_data = kwargs.get("json", {})

        response = self.client.request(
            method=method, 
            url=url, 
            headers=headers,
            json=request_data
        )
        response.raise_for_status()
        result: Dict[str, Any] = response.json()

        if result.get("return_code") != 0:
            raise Exception(f"API 요청 실패: {result.get('return_msg')}")

        return result

    def get_stock_price(self, stock_code: str) -> Dict[str, Any]:
        """
        주식 시세 정보를 조회합니다.
        API ID: tr10001
        """
        data = {
            "stock_code": stock_code
        }
        return self._make_request("POST", "tr10001", json=data)

    def get_stock_info(self, stock_code: str) -> Dict[str, Any]:
        """
        종목 기본 정보를 조회합니다.
        API ID: tr10002
        """
        data = {
            "stock_code": stock_code
        }
        return self._make_request("POST", "tr10002", json=data)

    def get_account_balance(self, account_number: str) -> Dict[str, Any]:
        """
        계좌 잔고를 조회합니다.
        API ID: ka10072
        
        Args:
            account_number (str): 계좌번호
            
        Returns:
            Dict[str, Any]: 계좌 잔고 정보
        """
        data = {
            "stk_cd": account_number,
            "strt_dt": datetime.now().strftime("%Y%m%d")
        }
        return self._make_request("POST", "ka10072", json=data)

    def get_order_history(self, account_number: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        일자별종목별실현손익요청_기간 내역을 조회합니다.
        API ID: ka10073
        
        Args:
            account_number (str): 계좌번호
            start_date (str): 시작일자 (YYYYMMDD)
            end_date (str): 종료일자 (YYYYMMDD)
            
        Returns:
            Dict[str, Any]: 주문 내역 정보
        """
        data = {
            "stk_cd": account_number,
            "strt_dt": start_date,
            "end_dt": end_date
        }
        return self._make_request("POST", "ka10073", json=data)

    def __del__(self) -> None:
        """
        클라이언트 연결을 종료합니다.
        """
        if hasattr(self, "client"):
            self.client.close()
