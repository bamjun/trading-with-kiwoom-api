from datetime import datetime
from typing import Any, Dict, Optional

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

    def _make_request(self, method: str, api_id: str, **kwargs: Any) -> Dict[str, Any]:
        """
        API 요청을 보내고 응답을 처리합니다.

        Args:
            method (str): HTTP 메서드 (GET, POST)
            api_id (str): API ID
            **kwargs: API 요청에 필요한 추가 파라미터
        """
        url = kwargs.get("url", f"{self.base_url}/api/dostk/acnt")
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json;charset=UTF-8",
            "api-id": api_id,
            "cont-yn": kwargs.get("cont_yn", "N"),
            "next-key": kwargs.get("next_key", ""),
        }

        # API 요청 데이터 구성
        request_data = kwargs.get("json", {})

        response = self.client.request(
            method=method, url=url, headers=headers, json=request_data
        )
        response.raise_for_status()
        result: Dict[str, Any] = response.json()

        if result.get("return_code") != 0:
            raise Exception(f"API 요청 실패: {result.get('return_msg')}")

        return result

    def basic_stock_information_request(self, stock_code: str) -> Dict[str, Any]:
        """
        주식 기본 정보를 조회합니다.
        API ID: ka10001

        Args:
            stock_code (str): 종목코드 (예: '005930')

        Returns:
            Dict[str, Any]: 주식 기본 정보
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code}
        return self._make_request("POST", "ka10001", url=url, json=data)

    def stock_trading_agent_request(self, stock_code: str) -> Dict[str, Any]:
        """
        주식거래원요청: 주식 거래원 정보를 조회합니다.
        API ID: ka10002

        Request Example:
            {
                "stk_cd": "005930"
            }

        Response Example:
            {
                "stk_cd":"005930",
                "stk_nm":"삼성전자",
                "cur_prc":"95400",
                "flu_smbol":"3",
                "base_pric":"95400",
                "pred_pre":"0",
                "flu_rt":"0.00",
                "sel_trde_ori_nm_1":"",
                "sel_trde_ori_1":"000",
                "sel_trde_qty_1":"0",
                "buy_trde_ori_nm_1":"",
                "buy_trde_ori_1":"000",
                "buy_trde_qty_1":"0",
                "sel_trde_ori_nm_2":"",
                "sel_trde_ori_2":"000",
                "sel_trde_qty_2":"0",
                "buy_trde_ori_nm_2":"",
                "buy_trde_ori_2":"000",
                "buy_trde_qty_2":"0",
                "sel_trde_ori_nm_3":"",
                "sel_trde_ori_3":"000",
                "sel_trde_qty_3":"0",
                "buy_trde_ori_nm_3":"",
                "buy_trde_ori_3":"000",
                "buy_trde_qty_3":"0",
                "sel_trde_ori_nm_4":"",
                "sel_trde_ori_4":"000",
                "sel_trde_qty_4":"0",
                "buy_trde_ori_nm_4":"",
                "buy_trde_ori_4":"000",
                "buy_trde_qty_4":"0",
                "sel_trde_ori_nm_5":"",
                "sel_trde_ori_5":"000",
                "sel_trde_qty_5":"0",
                "buy_trde_ori_nm_5":"",
                "buy_trde_ori_5":"000",
                "buy_trde_qty_5":"0",
                "return_code":0,
                "return_msg":"정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code}
        return self._make_request("POST", "ka10002", url=url, json=data)

    def trade_execution_information_request(self, stock_code: str) -> Dict[str, Any]:
        """
        주식 거래 실행 정보를 조회합니다.
        API ID: ka10003
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code}
        return self._make_request("POST", "ka10003", url=url, json=data)

    def credit_trading_trend_request(
        self, stock_code: str, date: str, query_type: str
    ) -> Dict[str, Any]:
        """
        신용매매동향요청: 신용 매매 동향 정보를 조회합니다.
        API ID: ka10013

        Args:
            stock_code (str): 종목코드 (예: '005930')
            date (str): 일자 (YYYYMMDD)
            query_type (str): 조회구분 (1:융자, 2:대주)

        Returns:
            Dict[str, Any]: 신용 매매 동향 정보

        Response Example:
            {
                "crd_trde_trend": [
                    {
                        "dt": "20241101",          # 일자
                        "cur_prc": "65100",        # 현재가
                        "pred_pre_sig": "0",       # 전일대비 부호
                        "pred_pre": "0",           # 전일대비
                        "trde_qty": "0",           # 거래량
                        "new": "",                 # 신규
                        "rpya": "",                # 상환
                        "remn": "",                # 잔고
                        "amt": "",                 # 금액
                        "pre": "",                 # 전일
                        "shr_rt": "",              # 비율
                        "remn_rt": ""              # 잔고비율
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code, "dt": date, "qry_tp": query_type}
        return self._make_request("POST", "ka10013", url=url, json=data)

    def get_stock_price(self, stock_code: str) -> Dict[str, Any]:
        """
        주식 시세 정보를 조회합니다.
        API ID: tr10001
        """
        data = {"stock_code": stock_code}
        return self._make_request("POST", "tr10001", json=data)

    def get_stock_info(self, stock_code: str) -> Dict[str, Any]:
        """
        종목 기본 정보를 조회합니다.
        API ID: tr10002
        """
        data = {"stock_code": stock_code}
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
        data = {"stk_cd": account_number, "strt_dt": datetime.now().strftime("%Y%m%d")}
        return self._make_request("POST", "ka10072", json=data)

    def get_order_history(
        self, account_number: str, start_date: str, end_date: str
    ) -> Dict[str, Any]:
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
        data = {"stk_cd": account_number, "strt_dt": start_date, "end_dt": end_date}
        return self._make_request("POST", "ka10073", json=data)

    def __del__(self) -> None:
        """
        클라이언트 연결을 종료합니다.
        """
        if hasattr(self, "client"):
            self.client.close()
