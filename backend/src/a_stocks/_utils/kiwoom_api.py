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

    def basic_stock_information_request_ka10001(
        self, stock_code: str
    ) -> Dict[str, Any]:
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

    def stock_trading_agent_request_ka10002(self, stock_code: str) -> Dict[str, Any]:
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

    def trade_execution_information_request_ka10003(
        self, stock_code: str
    ) -> Dict[str, Any]:
        """
        주식 거래 실행 정보를 조회합니다.
        API ID: ka10003
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code}
        return self._make_request("POST", "ka10003", url=url, json=data)

    def credit_trading_trend_request_ka10013(
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

    def daily_transaction_details_request_ka10015(
        self, stock_code: str, date: str
    ) -> Dict[str, Any]:
        """
        일별거래상세요청: 일별 거래 상세 정보를 조회합니다.
        API ID: ka10015

        Args:
            stock_code (str): 종목코드 (예: '005930')
            date (str): 시작일자 (YYYYMMDD)

        Returns:
            Dict[str, Any]: 일별 거래 상세 정보

        Response Example:
            {
                "daly_trde_dtl": [
                    {
                        "dt": "20241105",          # 일자
                        "close_pric": "135300",    # 종가
                        "pred_pre_sig": "0",       # 전일대비부호
                        "pred_pre": "0",           # 전일대비
                        "flu_rt": "0.00",          # 등락률
                        "trde_qty": "0",           # 거래량
                        "trde_prica": "0",         # 거래대금
                        "bf_mkrt_trde_qty": "",    # 시간외거래량
                        "opmr_trde_qty": "",       # 장중거래량
                        "af_mkrt_trde_qty": "",    # 장후거래량
                        "for_netprps": "",         # 외국인순매수
                        "orgn_netprps": "",        # 기관순매수
                        "ind_netprps": "",         # 개인순매수
                        "crd_remn_rt": ""          # 신용잔고율
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code, "strt_dt": date}
        return self._make_request("POST", "ka10015", url=url, json=data)

    def reported_low_price_request_ka10016(
        self,
        market_type: str = "000",
        new_high_low_type: str = "1",
        high_low_close_type: str = "1",
        stock_condition: str = "0",
        trade_qty_type: str = "00000",
        credit_condition: str = "0",
        include_up_down_limit: str = "0",
        period: str = "5",
        exchange_type: str = "1",
    ) -> Dict[str, Any]:
        """
        신고저가요청: 신고가/신저가 정보를 조회합니다.
        API ID: ka10016

        Args:
            market_type (str): 시장구분 (000:전체, 001:코스피, 101:코스닥)
            new_high_low_type (str): 신고저구분 (1:신고가, 2:신저가)
            high_low_close_type (str): 고저종구분 (1:고저기준, 2:종가기준)
            stock_condition (str): 종목조건 (0:전체조회, 1:관리종목제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기)
            trade_qty_type (str): 거래량구분 (00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상)
            credit_condition (str): 신용조건 (0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체)
            include_up_down_limit (str): 상하한포함 (0:미포함, 1:포함)
            period (str): 기간 (5:5일, 10:10일, 20:20일, 60:60일, 250:250일)
            exchange_type (str): 거래소구분 (1:KRX, 2:NXT, 3:통합)

        Returns:
            Dict[str, Any]: 신고저가 정보

        Response Example:
            {
                "ntl_pric": [
                    {
                        "stk_cd": "005930",        # 종목코드
                        "stk_nm": "삼성전자",       # 종목명
                        "cur_prc": "334",          # 현재가
                        "pred_pre_sig": "3",       # 전일대비부호
                        "pred_pre": "0",           # 전일대비
                        "flu_rt": "0.00",          # 등락률
                        "trde_qty": "3",           # 거래량
                        "pred_trde_qty_pre_rt": "-0.00", # 전일거래량대비율
                        "sel_bid": "0",            # 매도호가
                        "buy_bid": "0",            # 매수호가
                        "high_pric": "334",        # 고가
                        "low_pric": "320"          # 저가
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {
            "mrkt_tp": market_type,
            "ntl_tp": new_high_low_type,
            "high_low_close_tp": high_low_close_type,
            "stk_cnd": stock_condition,
            "trde_qty_tp": trade_qty_type,
            "crd_cnd": credit_condition,
            "updown_incls": include_up_down_limit,
            "dt": period,
            "stex_tp": exchange_type,
        }
        return self._make_request("POST", "ka10016", url=url, json=data)

    def upper_lower_limit_price_request_ka10017(
        self,
        market_type: str = "000",
        updown_type: str = "1",
        sort_type: str = "1",
        stock_condition: str = "0",
        trade_qty_type: str = "00000",
        credit_condition: str = "0",
        trade_gold_type: str = "0",
        exchange_type: str = "1",
    ) -> Dict[str, Any]:
        """
        상한/하한가요청: 상한/하한가 정보를 조회합니다.
        API ID: ka10017

        Args:
            market_type (str): 시장구분 (000:전체, 001:코스피, 101:코스닥)
            updown_type (str): 상하한구분 (1:상한, 2:상승, 3:보합, 4:하한, 5:하락, 6:전일상한, 7:전일하한)
            sort_type (str): 정렬구분 (1:종목코드순, 2:연속횟수순(상위100개), 3:등락률순)
            stock_condition (str): 종목조건 (0:전체조회, 1:관리종목제외, 3:우선주제외, 4:우선주+관리종목제외, 5:증100제외, 6:증100만 보기, 7:증40만 보기, 8:증30만 보기, 9:증20만 보기, 10:우선주+관리종목+환기종목제외)
            trade_qty_type (str): 거래량구분 (00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상)
            credit_condition (str): 신용조건 (0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체)
            trade_gold_type (str): 매매금구분 (0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~3천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상)
            exchange_type (str): 거래소구분 (1:KRX, 2:NXT, 3:통합)

        Returns:
            Dict[str, Any]: 상하한가 정보

        Response Example:
            {
                "updown_pric": [
                    {
                        "stk_cd": "005930",        # 종목코드
                        "stk_infr": "",            # 종목정보
                        "stk_nm": "삼성전자",       # 종목명
                        "cur_prc": "+235500",      # 현재가
                        "pred_pre_sig": "1",       # 전일대비기호
                        "pred_pre": "+54200",      # 전일대비
                        "flu_rt": "+29.90",        # 등락률
                        "trde_qty": "0",           # 거래량
                        "pred_trde_qty": "96197",  # 전일거래량
                        "sel_req": "0",            # 매도잔량
                        "sel_bid": "0",            # 매도호가
                        "buy_bid": "+235500",      # 매수호가
                        "buy_req": "4",            # 매수잔량
                        "cnt": "1"                 # 횟수
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {
            "mrkt_tp": market_type,
            "updown_tp": updown_type,
            "sort_tp": sort_type,
            "stk_cnd": stock_condition,
            "trde_qty_tp": trade_qty_type,
            "crd_cnd": credit_condition,
            "trde_gold_tp": trade_gold_type,
            "stex_tp": exchange_type,
        }
        return self._make_request("POST", "ka10017", url=url, json=data)

    def near_high_low_price_request_ka10018(
        self,
        high_low_type: str,
        proximity_rate: str,
        market_type: str,
        trade_qty_type: str,
        stock_condition: str,
        credit_condition: str,
        exchange_type: str,
    ) -> Dict[str, Any]:
        """
        근접고저가요청: 근접고저가 정보를 조회합니다.
        API ID: ka10018

        Args:
            high_low_type (str): 고저구분 (1:고가, 2:저가)
            proximity_rate (str): 근접율 (05:0.5, 10:1.0, 15:1.5, 20:2.0, 25:2.5, 30:3.0)
            market_type (str): 시장구분 (000:전체, 001:코스피, 101:코스닥)
            trade_qty_type (str): 거래량구분 (00000:전체, 00010:만주이상, 00050:5만주이상 등)
            stock_condition (str): 종목조건 (0:전체, 1:관리종목제외 등)
            credit_condition (str): 신용조건 (0:전체, 1:신용융자A군 등)
            exchange_type (str): 거래소구분 (1:KRX, 2:NXT, 3:통합)

        Returns:
            Dict[str, Any]: 근접고저가 정보

        Response Example:
            {
                "high_low_pric_alacc": [
                    {
                        "stk_cd": "004930",        # 종목코드
                        "stk_nm": "삼성전자",        # 종목명
                        "cur_prc": "334",          # 현재가
                        "pred_pre_sig": "0",       # 전일대비기호
                        "pred_pre": "0",           # 전일대비
                        "flu_rt": "0.00",          # 등락률
                        "trde_qty": "3",           # 거래량
                        "sel_bid": "0",            # 매도호가
                        "buy_bid": "0",            # 매수호가
                        "tdy_high_pric": "334",    # 당일고가
                        "tdy_low_pric": "334"      # 당일저가
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {
            "high_low_tp": high_low_type,
            "alacc_rt": proximity_rate,
            "mrkt_tp": market_type,
            "trde_qty_tp": trade_qty_type,
            "stk_cnd": stock_condition,
            "crd_cnd": credit_condition,
            "stex_tp": exchange_type,
        }
        return self._make_request("POST", "ka10018", url=url, json=data)

    def rapid_price_change_request_ka10019(
        self,
        market_type: str,
        fluctuation_type: str,
        time_type: str,
        time: str,
        trade_qty_type: str,
        stock_condition: str,
        credit_condition: str,
        price_condition: str,
        include_up_down_limit: str,
        exchange_type: str,
    ) -> Dict[str, Any]:
        """
        가격급등락요청: 급등/급락 종목 정보를 조회합니다.
        API ID: ka10019

        Args:
            market_type (str): 시장구분 (000:전체, 001:코스피, 101:코스닥, 201:코스피200)
            fluctuation_type (str): 등락구분 (1:급등, 2:급락)
            time_type (str): 시간구분 (1:분전, 2:일전)
            time (str): 시간 (분 혹은 일입력)
            trade_qty_type (str): 거래량구분 (00000:전체조회, 00010:만주이상 등)
            stock_condition (str): 종목조건 (0:전체조회, 1:관리종목제외 등)
            credit_condition (str): 신용조건 (0:전체조회, 1:신용융자A군 등)
            price_condition (str): 가격조건 (0:전체조회, 1:1천원미만 등)
            include_up_down_limit (str): 상하한포함 (0:미포함, 1:포함)
            exchange_type (str): 거래소구분 (1:KRX, 2:NXT, 3:통합)

        Returns:
            Dict[str, Any]: 가격급등락 정보

        Response Example:
            {
                "pric_jmpflu": [
                    {
                        "stk_cd": "005930",        # 종목코드
                        "stk_cls": "",             # 종목분류
                        "stk_nm": "삼성전자",        # 종목명
                        "pred_pre_sig": "2",       # 전일대비기호
                        "pred_pre": "+300",        # 전일대비
                        "flu_rt": "+0.57",         # 등락률
                        "base_pric": "51600",      # 기준가
                        "cur_prc": "+52700",       # 현재가
                        "base_pre": "1100",        # 기준대비
                        "trde_qty": "2400",        # 거래량
                        "jmp_rt": "+2.13"          # 급등률
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {
            "mrkt_tp": market_type,
            "flu_tp": fluctuation_type,
            "tm_tp": time_type,
            "tm": time,
            "trde_qty_tp": trade_qty_type,
            "stk_cnd": stock_condition,
            "crd_cnd": credit_condition,
            "pric_cnd": price_condition,
            "updown_incls": include_up_down_limit,
            "stex_tp": exchange_type,
        }
        return self._make_request("POST", "ka10019", url=url, json=data)

    def trading_volume_update_request_ka10024(
        self, market_type: str, cycle_type: str, trade_qty_type: str, exchange_type: str
    ) -> Dict[str, Any]:
        """
        거래량갱신요청: 거래량 갱신 정보를 조회합니다.
        API ID: ka10024

        Args:
            market_type (str): 시장구분 (000:전체, 001:코스피, 101:코스닥)
            cycle_type (str): 주기구분 (5:5일, 10:10일, 20:20일, 60:60일, 250:250일)
            trade_qty_type (str): 거래량구분 (5:5천주이상, 10:만주이상, 50:5만주이상 등)
            exchange_type (str): 거래소구분 (1:KRX, 2:NXT, 3:통합)

        Returns:
            Dict[str, Any]: 거래량 갱신 정보

        Response Example:
            {
                "trde_qty_updt": [
                    {
                        "stk_cd": "005930",        # 종목코드
                        "stk_nm": "삼성전자",        # 종목명
                        "cur_prc": "+74800",       # 현재가
                        "pred_pre_sig": "1",       # 전일대비기호
                        "pred_pre": "+17200",      # 전일대비
                        "flu_rt": "+29.86",        # 등락률
                        "prev_trde_qty": "243520", # 이전거래량
                        "now_trde_qty": "435771",  # 현재거래량
                        "sel_bid": "0",            # 매도호가
                        "buy_bid": "+74800"        # 매수호가
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {
            "mrkt_tp": market_type,
            "cycle_tp": cycle_type,
            "trde_qty_tp": trade_qty_type,
            "stex_tp": exchange_type,
        }
        return self._make_request("POST", "ka10024", url=url, json=data)

    def supply_concentration_request_ka10025(
        self,
        market_type: str,
        supply_concentration_rate: str,
        current_price_entry: str,
        supply_count: str,
        cycle_type: str,
        exchange_type: str,
    ) -> Dict[str, Any]:
        """
        매물대집중요청: 매물대 집중 정보를 조회합니다.
        API ID: ka10025

        Args:
            market_type (str): 시장구분 (000:전체, 001:코스피, 101:코스닥)
            supply_concentration_rate (str): 매물집중비율 (0~100 입력)
            current_price_entry (str): 현재가진입 (0:포함안함, 1:포함)
            supply_count (str): 매물대수 (숫자입력)
            cycle_type (str): 주기구분 (50:50일, 100:100일, 150:150일, 200:200일, 250:250일, 300:300일)
            exchange_type (str): 거래소구분 (1:KRX, 2:NXT, 3:통합)

        Returns:
            Dict[str, Any]: 매물대 집중 정보

        Response Example:
            {
                "prps_cnctr": [
                    {
                        "stk_cd": "005930",        # 종목코드
                        "stk_nm": "삼성전자",        # 종목명
                        "cur_prc": "30000",        # 현재가
                        "pred_pre_sig": "3",       # 전일대비기호
                        "pred_pre": "0",           # 전일대비
                        "flu_rt": "0.00",          # 등락률
                        "now_trde_qty": "0",       # 현재거래량
                        "pric_strt": "31350",      # 가격대시작
                        "pric_end": "31799",       # 가격대끝
                        "prps_qty": "4",           # 매물량
                        "prps_rt": "+50.00"        # 매물비
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {
            "mrkt_tp": market_type,
            "prps_cnctr_rt": supply_concentration_rate,
            "cur_prc_entry": current_price_entry,
            "prpscnt": supply_count,
            "cycle_tp": cycle_type,
            "stex_tp": exchange_type,
        }
        return self._make_request("POST", "ka10025", url=url, json=data)

    def high_low_per_request_ka10026(
        self, per_type: str, exchange_type: str
    ) -> Dict[str, Any]:
        """
        고저PER요청: 고저PER 정보를 조회합니다.
        API ID: ka10026

        Args:
            per_type (str): PER구분 (1:저PBR, 2:고PBR, 3:저PER, 4:고PER, 5:저ROE, 6:고ROE)
            exchange_type (str): 거래소구분 (1:KRX, 2:NXT, 3:통합)

        Returns:
            Dict[str, Any]: 고저PER 정보

        Response Example:
            {
                "high_low_per": [
                    {
                        "stk_cd": "005930",        # 종목코드
                        "stk_nm": "삼성전자",        # 종목명
                        "per": "0.44",             # PER
                        "cur_prc": "4930",         # 현재가
                        "pred_pre_sig": "3",       # 전일대비기호
                        "pred_pre": "0",           # 전일대비
                        "flu_rt": "0.00",          # 등락률
                        "now_trde_qty": "0",       # 현재거래량
                        "sel_bid": "0"             # 매도호가
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"pertp": per_type, "stex_tp": exchange_type}
        return self._make_request("POST", "ka10026", url=url, json=data)

    def rate_of_change_compared_to_opening_price_request_ka10028(
        self,
        sort_type: str,
        trade_qty_condition: str,
        market_type: str,
        include_up_down_limit: str,
        stock_condition: str,
        credit_condition: str,
        trade_price_condition: str,
        fluctuation_condition: str,
        exchange_type: str,
    ) -> Dict[str, Any]:
        """
        시가대비등락률요청: 시가대비 등락률 정보를 조회합니다.
        API ID: ka10028

        Args:
            sort_type (str): 정렬구분 (1:시가, 2:고가, 3:저가, 4:기준가)
            trade_qty_condition (str): 거래량조건 (0000:전체, 0010:만주이상 등)
            market_type (str): 시장구분 (000:전체, 001:코스피, 101:코스닥)
            include_up_down_limit (str): 상하한포함 (0:불포함, 1:포함)
            stock_condition (str): 종목조건 (0:전체, 1:관리종목제외 등)
            credit_condition (str): 신용조건 (0:전체, 1:신용융자A군 등)
            trade_price_condition (str): 거래대금조건 (0:전체, 3:3천만원이상 등)
            fluctuation_condition (str): 등락조건 (1:상위, 2:하위)
            exchange_type (str): 거래소구분 (1:KRX, 2:NXT, 3:통합)

        Returns:
            Dict[str, Any]: 시가대비 등락률 정보

        Response Example:
            {
                "open_pric_pre_flu_rt": [
                    {
                        "stk_cd": "005930",        # 종목코드
                        "stk_nm": "삼성전자",        # 종목명
                        "cur_prc": "+74800",       # 현재가
                        "pred_pre_sig": "1",       # 전일대비기호
                        "pred_pre": "+17200",      # 전일대비
                        "flu_rt": "+29.86",        # 등락률
                        "open_pric": "+65000",     # 시가
                        "high_pric": "+74800",     # 고가
                        "low_pric": "-57000",      # 저가
                        "open_pric_pre": "+15.08", # 시가대비
                        "now_trde_qty": "448203",  # 현재거래량
                        "cntr_str": "346.54"       # 체결강도
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {
            "sort_tp": sort_type,
            "trde_qty_cnd": trade_qty_condition,
            "mrkt_tp": market_type,
            "updown_incls": include_up_down_limit,
            "stk_cnd": stock_condition,
            "crd_cnd": credit_condition,
            "trde_prica_cnd": trade_price_condition,
            "flu_cnd": fluctuation_condition,
            "stex_tp": exchange_type,
        }
        return self._make_request("POST", "ka10028", url=url, json=data)

    def trading_agent_supply_demand_analysis_request_ka10043(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        query_date_type: str,
        point_type: str,
        date: str,
        sort_base: str,
        member_code: str,
        exchange_type: str,
    ) -> Dict[str, Any]:
        """
        거래원매물대분석요청: 거래원 매물대 분석 정보를 조회합니다.
        API ID: ka10043

        Args:
            stock_code (str): 종목코드
            start_date (str): 시작일자 (YYYYMMDD)
            end_date (str): 종료일자 (YYYYMMDD)
            query_date_type (str): 조회기간구분 (0:기간으로 조회, 1:시작일자, 종료일자로 조회)
            point_type (str): 시점구분 (0:당일, 1:전일)
            date (str): 기간 (5:5일, 10:10일, 20:20일, 40:40일, 60:60일, 120:120일)
            sort_base (str): 정렬기준 (1:종가순, 2:날짜순)
            member_code (str): 회원사코드
            exchange_type (str): 거래소구분 (1:KRX, 2:NXT, 3:통합)

        Returns:
            Dict[str, Any]: 거래원 매물대 분석 정보

        Response Example:
            {
                "trde_ori_prps_anly": [
                    {
                        "dt": "20241105",        # 일자
                        "close_pric": "135300",  # 종가
                        "pre_sig": "2",          # 대비기호
                        "pred_pre": "+1700",     # 전일대비
                        "sel_qty": "43",         # 매도량
                        "buy_qty": "1090",       # 매수량
                        "netprps_qty": "1047",   # 순매수수량
                        "trde_qty_sum": "1133",  # 거래량합
                        "trde_wght": "+1317.44"  # 거래비중
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {
            "stk_cd": stock_code,
            "strt_dt": start_date,
            "end_dt": end_date,
            "qry_dt_tp": query_date_type,
            "pot_tp": point_type,
            "dt": date,
            "sort_base": sort_base,
            "mmcm_cd": member_code,
            "stex_tp": exchange_type,
        }
        return self._make_request("POST", "ka10043", url=url, json=data)

    def trading_agent_instant_trading_volume_request_ka10052(
        self,
        member_code: str,
        stock_code: str = "",
        market_type: str = "0",
        quantity_type: str = "0",
        price_type: str = "0",
        exchange_type: str = "3",
    ) -> Dict[str, Any]:
        """
        거래원순간거래량요청: 거래원 순간 거래량 정보를 조회합니다.
        API ID: ka10052

        Args:
            member_code (str): 회원사코드
            stock_code (str, optional): 종목코드. 기본값은 "".
            market_type (str, optional): 시장구분 (0:전체, 1:코스피, 2:코스닥, 3:종목). 기본값은 "0".
            quantity_type (str, optional): 수량구분 (0:전체, 1:1000주, 2:2000주 등). 기본값은 "0".
            price_type (str, optional): 가격구분 (0:전체, 1:1천원 미만 등). 기본값은 "0".
            exchange_type (str, optional): 거래소구분 (1:KRX, 2:NXT, 3:통합). 기본값은 "3".

        Returns:
            Dict[str, Any]: 거래원 순간 거래량 정보

        Response Example:
            {
                "trde_ori_mont_trde_qty": [
                    {
                        "tm": "161437",            # 시간
                        "stk_cd": "005930",        # 종목코드
                        "stk_nm": "삼성전자",        # 종목명
                        "trde_ori_nm": "다이와",     # 거래원명
                        "tp": "-매도",              # 구분
                        "mont_trde_qty": "-399928", # 순간거래량
                        "acc_netprps": "-1073004",  # 누적순매수
                        "cur_prc": "+57700",        # 현재가
                        "pred_pre_sig": "2",        # 전일대비기호
                        "pred_pre": "400",          # 전일대비
                        "flu_rt": "+0.70"           # 등락율
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {
            "mmcm_cd": member_code,
            "stk_cd": stock_code,
            "mrkt_tp": market_type,
            "qty_tp": quantity_type,
            "pric_tp": price_type,
            "stex_tp": exchange_type,
        }
        return self._make_request("POST", "ka10052", url=url, json=data)

    def volatility_mitigation_device_triggered_stocks_request_ka10054(
        self,
        market_type: str,
        before_market_type: str,
        stock_code: str = "",
        motion_type: str = "0",
        skip_stocks: str = "000000000",
        trade_qty_type: str = "0",
        min_trade_qty: str = "0",
        max_trade_qty: str = "0",
        trade_price_type: str = "0",
        min_trade_price: str = "0",
        max_trade_price: str = "0",
        motion_direction: str = "0",
        exchange_type: str = "3",
    ) -> Dict[str, Any]:
        """
        변동성완화장치발동종목요청: 변동성 완화 장치 작동 종목 정보를 조회합니다.
        API ID: ka10054

        Args:
            market_type (str): 시장구분 (000:전체, 001:코스피, 101:코스닥)
            before_market_type (str): 장전구분 (0:전체, 1:정규시장, 2:시간외단일가)
            stock_code (str, optional): 종목코드. 기본값은 "".
            motion_type (str, optional): 발동구분 (0:전체, 1:정적VI, 2:동적VI, 3:동적VI+정적VI). 기본값은 "0".
            skip_stocks (str, optional): 제외종목. 기본값은 "000000000".
            trade_qty_type (str, optional): 거래량구분 (0:사용안함, 1:사용). 기본값은 "0".
            min_trade_qty (str, optional): 최소거래량. 기본값은 "0".
            max_trade_qty (str, optional): 최대거래량. 기본값은 "0".
            trade_price_type (str, optional): 거래대금구분 (0:사용안함, 1:사용). 기본값은 "0".
            min_trade_price (str, optional): 최소거래대금. 기본값은 "0".
            max_trade_price (str, optional): 최대거래대금. 기본값은 "0".
            motion_direction (str, optional): 발동방향 (0:전체, 1:상승, 2:하락). 기본값은 "0".
            exchange_type (str, optional): 거래소구분 (1:KRX, 2:NXT, 3:통합). 기본값은 "3".

        Returns:
            Dict[str, Any]: 변동성 완화 장치 작동 종목 정보

        Response Example:
            {
                "motn_stk": [
                    {
                        "stk_cd": "005930",             # 종목코드
                        "stk_nm": "삼성전자",             # 종목명
                        "acc_trde_qty": "1105968",      # 누적거래량
                        "motn_pric": "67000",           # 발동가격
                        "dynm_dispty_rt": "+9.30",      # 동적괴리율
                        "trde_cntr_proc_time": "172311", # 매매체결처리시각
                        "virelis_time": "172511",       # VI해제시각
                        "viaplc_tp": "동적",             # VI적용구분
                        "dynm_stdpc": "61300",          # 동적기준가격
                        "static_stdpc": "0",            # 정적기준가격
                        "static_dispty_rt": "0.00",     # 정적괴리율
                        "open_pric_pre_flu_rt": "+16.93", # 시가대비등락률
                        "vimotn_cnt": "23",             # VI발동횟수
                        "stex_tp": "NXT"                # 거래소구분
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {
            "mrkt_tp": market_type,
            "bf_mkrt_tp": before_market_type,
            "stk_cd": stock_code,
            "motn_tp": motion_type,
            "skip_stk": skip_stocks,
            "trde_qty_tp": trade_qty_type,
            "min_trde_qty": min_trade_qty,
            "max_trde_qty": max_trade_qty,
            "trde_prica_tp": trade_price_type,
            "min_trde_prica": min_trade_price,
            "max_trde_prica": max_trade_price,
            "motn_drc": motion_direction,
            "stex_tp": exchange_type,
        }
        return self._make_request("POST", "ka10054", url=url, json=data)

    def today_vs_previous_day_execution_volume_request_ka10055(
        self, stock_code: str, today_previous: str
    ) -> Dict[str, Any]:
        """
        당일전일체결량요청: 당일 및 전일 체결량 정보를 조회합니다.
        API ID: ka10055

        Args:
            stock_code (str): 종목코드
            today_previous (str): 당일전일 (1:당일, 2:전일)

        Returns:
            Dict[str, Any]: 당일/전일 체결량 정보

        Response Example:
            {
                "tdy_pred_cntr_qty": [
                    {
                        "cntr_tm": "171945",          # 체결시간
                        "cntr_pric": "+74800",        # 체결가
                        "pred_pre_sig": "1",          # 전일대비기호
                        "pred_pre": "+17200",         # 전일대비
                        "flu_rt": "+29.86",           # 등락율
                        "cntr_qty": "-1793",          # 체결량
                        "acc_trde_qty": "446203",     # 누적거래량
                        "acc_trde_prica": "33225"     # 누적거래대금
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code, "tdy_pred": today_previous}
        return self._make_request("POST", "ka10055", url=url, json=data)

    def daily_trading_stocks_by_investor_type_request_ka10058(
        self,
        start_date: str,
        end_date: str,
        trade_type: str,
        market_type: str,
        investor_type: str,
        exchange_type: str,
    ) -> Dict[str, Any]:
        """
        투자자별일별매매종목요청: 투자자유형별 일자별 거래량 정보를 조회합니다.
        API ID: ka10058

        Args:
            start_date (str): 시작일자 (YYYYMMDD)
            end_date (str): 종료일자 (YYYYMMDD)
            trade_type (str): 매매구분 (순매도:1, 순매수:2)
            market_type (str): 시장구분 (001:코스피, 101:코스닥)
            investor_type (str): 투자자구분 (8000:개인, 9000:외국인, 1000:금융투자 등)
            exchange_type (str): 거래소구분 (1:KRX, 2:NXT, 3:통합)

        Returns:
            Dict[str, Any]: 투자자별 일별 매매종목 정보

        Response Example:
            {
                "invsr_daly_trde_stk": [
                    {
                        "stk_cd": "005930",       # 종목코드
                        "stk_nm": "삼성전자",       # 종목명
                        "netslmt_qty": "+4464",   # 순매도수량
                        "netslmt_amt": "+25467",  # 순매도금액
                        "prsm_avg_pric": "57056", # 추정평균가
                        "cur_prc": "+61300",      # 현재가
                        "pre_sig": "2",           # 대비기호
                        "pred_pre": "+4000",      # 전일대비
                        "avg_pric_pre": "+4244",  # 평균가대비
                        "pre_rt": "+7.43",        # 대비율
                        "dt_trde_qty": "1554171"  # 기간거래량
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {
            "strt_dt": start_date,
            "end_dt": end_date,
            "trde_tp": trade_type,
            "mrkt_tp": market_type,
            "invsr_tp": investor_type,
            "stex_tp": exchange_type,
        }
        return self._make_request("POST", "ka10058", url=url, json=data)

    def stock_data_by_investor_institution_request_ka10059(
        self,
        date: str,
        stock_code: str,
        amount_quantity_type: str,
        trade_type: str,
        unit_type: str,
    ) -> Dict[str, Any]:
        """
        종목별투자자기관별요청: 투자기관별 종목별 거래량 정보를 조회합니다.
        API ID: ka10059

        Args:
            date (str): 일자 (YYYYMMDD)
            stock_code (str): 종목코드
            amount_quantity_type (str): 금액수량구분 (1:금액, 2:수량)
            trade_type (str): 매매구분 (0:순매수, 1:매수, 2:매도)
            unit_type (str): 단위구분 (1000:천주, 1:단주)

        Returns:
            Dict[str, Any]: 종목별 투자자/기관별 정보

        Response Example:
            {
                "stk_invsr_orgn": [
                    {
                        "dt": "20241107",            # 일자
                        "cur_prc": "+61300",         # 현재가
                        "pre_sig": "2",              # 대비기호
                        "pred_pre": "+4000",         # 전일대비
                        "flu_rt": "+698",            # 등락율
                        "acc_trde_qty": "1105968",   # 누적거래량
                        "acc_trde_prica": "64215",   # 누적거래대금
                        "ind_invsr": "1584",         # 개인투자자
                        "frgnr_invsr": "-61779",     # 외국인투자자
                        "orgn": "60195",             # 기관계
                        "fnnc_invt": "25514",        # 금융투자
                        "insrnc": "0",               # 보험
                        "invtrt": "0",               # 투신
                        "etc_fnnc": "34619",         # 기타금융
                        "bank": "4",                 # 은행
                        "penfnd_etc": "-1",          # 연기금등
                        "samo_fund": "58",           # 사모펀드
                        "natn": "0",                 # 국가
                        "etc_corp": "0",             # 기타법인
                        "natfor": "1"                # 내외국인
                    },
                    # 추가 데이터...
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {
            "dt": date,
            "stk_cd": stock_code,
            "amt_qty_tp": amount_quantity_type,
            "trde_tp": trade_type,
            "unit_tp": unit_type,
        }
        return self._make_request("POST", "ka10059", url=url, json=data)
    
    
    def aggregate_stock_data_by_investor_institution_request_ka10061(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        amount_quantity_type: str,
        trade_type: str,
        unit_type: str,
    ) -> Dict[str, Any]:
        """
        종목별투자자기관별합계요청: 투자자유형별 종목별 거래량 합계 정보를 조회합니다.
        API ID: ka10061

        Args:
            stock_code (str): 종목코드 (예: '005930')
            start_date (str): 시작일자 (YYYYMMDD)
            end_date (str): 종료일자 (YYYYMMDD)
            amount_quantity_type (str): 금액수량구분 (1:금액, 2:수량)
            trade_type (str): 매매구분 (0:순매수, 1:매수, 2:매도)
            unit_type (str): 단위구분 (1000:천주, 1:단주)

        Returns:
            Dict[str, Any]: 종목별 투자자/기관별 합계 정보

        Response Example:
            {
                "stk_invsr_orgn_tot": [
                    {
                        "ind_invsr": "--28837",       # 개인투자자
                        "frgnr_invsr": "--40142",     # 외국인투자자
                        "orgn": "+64891",             # 기관계
                        "fnnc_invt": "+72584",        # 금융투자
                        "insrnc": "--9071",           # 보험
                        "invtrt": "--7790",           # 투신
                        "etc_fnnc": "+35307",         # 기타금융
                        "bank": "+526",               # 은행
                        "penfnd_etc": "--22783",      # 연기금등
                        "samo_fund": "--3881",        # 사모펀드
                        "natn": "0",                  # 국가
                        "etc_corp": "+1974",          # 기타법인
                        "natfor": "+2114"             # 내외국인
                    }
                ],
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {
            "stk_cd": stock_code,
            "strt_dt": start_date,
            "end_dt": end_date,
            "amt_qty_tp": amount_quantity_type,
            "trde_tp": trade_type,
            "unit_tp": unit_type,
        }
        return self._make_request("POST", "ka10061", url=url, json=data)
    
    def today_vs_previous_day_execution_request_ka10084(
        self,
        stock_code: str,
        today_previous: str,
        tick_minute: str,
        time: str = "",
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code, "tdy_pred": today_previous, "tic_min": tick_minute, "tm": time}
        return self._make_request("POST", "ka10084", url=url, json=data)
    
    def watchlist_stock_information_request_ka10095(
        self,
        stock_code: str,
    ) -> Dict[str, Any]:
        """
        종목별종목정보요청: 종목별 종목정보를 조회합니다.
        API ID: ka10095
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code}
        return self._make_request("POST", "ka10095", url=url, json=data)
    
    def stock_information_list_request_ka10099(
        self,
        stock_code: str,
    ) -> Dict[str, Any]:
        """
        종목정보목록요청: 종목정보목록을 조회합니다.
        API ID: ka10099
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code}
        return self._make_request("POST", "ka10099", url=url, json=data)

    def stock_information_inquiry_ka10100(
        self,
        stock_code: str,
    ) -> Dict[str, Any]:
        """
        종목정보조회요청: 종목정보를 조회합니다.
        API ID: ka10100
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code}
        return self._make_request("POST", "ka10100", url=url, json=data)

    def industry_code_list_ka10101(
        self,
        stock_code: str,
    ) -> Dict[str, Any]:
        """
        산업코드목록요청: 산업코드목록을 조회합니다.
        API ID: ka10101
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code}
        return self._make_request("POST", "ka10101", url=url, json=data)

    def member_company_list_ka10102(
        self,
        stock_code: str,
    ) -> Dict[str, Any]:
        """
        주식시세정보요청: 주식시세정보를 조회합니다.
        API ID: ka10102
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code}
        return self._make_request("POST", "ka10102", url=url, json=data)

    def top_50_program_buy_request_ka90003(
        self,
        stock_code: str,
    ) -> Dict[str, Any]:
        """
        상위50프로그램매수요청: 상위50프로그램매수를 조회합니다.
        API ID: ka90003
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code}
        return self._make_request("POST", "ka90003", url=url, json=data)

    def stock_wise_program_trading_status_request_ka90004(
        self,
        stock_code: str,
    ) -> Dict[str, Any]:
        """
        종목별프로그램매매상태요청: 종목별프로그램매매상태를 조회합니다.
        API ID: ka90004
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code}
        return self._make_request("POST", "ka90004", url=url, json=data)
    
    def margin_trading_transaction_details_request_ka90012(
        self,
        stock_code: str,
    ) -> Dict[str, Any]:
        """
        매매기관매매상세요청: 매매기관매매상세를 조회합니다.
        API ID: ka90012
        """
        url = f"{self.base_url}/api/dostk/stkinfo"
        data = {"stk_cd": stock_code}
        return self._make_request("POST", "ka90012", url=url, json=data)

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
