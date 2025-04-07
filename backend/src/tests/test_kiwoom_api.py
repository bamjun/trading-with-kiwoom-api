from datetime import datetime, timedelta

import pytest
from pytest_mock import MockerFixture

from a_stocks._utils.kiwoom_api import KiwoomAPI


@pytest.fixture
def kiwoom_api() -> KiwoomAPI:
    return KiwoomAPI()


def test_basic_stock_information_request_success_ka10001(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "stk_cd": "005930",
        "stk_nm": "삼성전자",
        "setl_mm": "12",
        "fav": "5000",
        "cap": "1311",
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response  # 토큰 요청용
    client_mock.request.return_value = api_response  # API 요청용

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.basic_stock_information_request_ka10001("005930")
    print(result)

    # Assert
    assert result["stk_cd"] == "005930"
    assert result["stk_nm"] == "삼성전자"
    assert result["return_code"] == 0
    assert result["return_msg"] == "정상적으로 처리되었습니다"


def test_stock_trading_agent_request_success_ka10002(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "stk_cd": "005930",
        "stk_nm": "삼성전자",
        "cur_prc": "95400",
        "flu_smbol": "3",
        "base_pric": "95400",
        "pred_pre": "0",
        "flu_rt": "0.00",
        "sel_trde_ori_nm_1": "",
        "sel_trde_ori_1": "000",
        "sel_trde_qty_1": "0",
        "buy_trde_ori_nm_1": "",
        "buy_trde_ori_1": "000",
        "buy_trde_qty_1": "0",
        "sel_trde_ori_nm_2": "",
        "sel_trde_ori_2": "000",
        "sel_trde_qty_2": "0",
        "buy_trde_ori_nm_2": "",
        "buy_trde_ori_2": "000",
        "buy_trde_qty_2": "0",
        "sel_trde_ori_nm_3": "",
        "sel_trde_ori_3": "000",
        "sel_trde_qty_3": "0",
        "buy_trde_ori_nm_3": "",
        "buy_trde_ori_3": "000",
        "buy_trde_qty_3": "0",
        "sel_trde_ori_nm_4": "",
        "sel_trde_ori_4": "000",
        "sel_trde_qty_4": "0",
        "buy_trde_ori_nm_4": "",
        "buy_trde_ori_4": "000",
        "buy_trde_qty_4": "0",
        "sel_trde_ori_nm_5": "",
        "sel_trde_ori_5": "000",
        "sel_trde_qty_5": "0",
        "buy_trde_ori_nm_5": "",
        "buy_trde_ori_5": "000",
        "buy_trde_qty_5": "0",
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()

    # post 메서드는 토큰 요청용
    client_mock.post.return_value = token_response

    # request 메서드는 API 요청용
    client_mock.request.return_value = api_response

    # httpx.Client 클래스 자체를 모킹하여 위에서 생성한 모킹된 클라이언트를 반환하도록 함
    mocker.patch("httpx.Client", return_value=client_mock)

    # 이미 생성된 kiwoom_api 인스턴스에 모킹된 client를 주입
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.stock_trading_agent_request_ka10002("005930")

    # Assert
    assert result["stk_cd"] == "005930"
    assert result["stk_nm"] == "삼성전자"
    assert result["return_code"] == 0

    # 실제 HTTP 요청에 전달된 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    assert call_args[1]["json"] == {"stk_cd": "005930"}


def test_trade_execution_information_request_success_ka10003(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "cntr_infr": [
            {
                "tm": "130429",
                "cur_prc": "+53500",
                "pred_pre": "+500",
                "pre_rt": "+0.94",
                "pri_sel_bid_unit": "+68900",
                "pri_buy_bid_unit": "+53500",
                "cntr_trde_qty": "1010",
                "sign": "2",
                "acc_trde_qty": "8735",
                "acc_trde_prica": "524269500",
                "cntr_str": "12.99",
                "stex_tp": "KRX",
            },
            {
                "tm": "130153",
                "cur_prc": "+68900",
                "pred_pre": "+15900",
                "pre_rt": "+30.00",
                "pri_sel_bid_unit": "+68900",
                "pri_buy_bid_unit": "+55000",
                "cntr_trde_qty": "456",
                "sign": "1",
                "acc_trde_qty": "7725",
                "acc_trde_prica": "470234500",
                "cntr_str": "12.99",
                "stex_tp": "KRX",
            },
            {
                "tm": "125947",
                "cur_prc": "+55000",
                "pred_pre": "+2000",
                "pre_rt": "+3.77",
                "pri_sel_bid_unit": "+68900",
                "pri_buy_bid_unit": "+55000",
                "cntr_trde_qty": "1000",
                "sign": "2",
                "acc_trde_qty": "7269",
                "acc_trde_prica": "438816100",
                "cntr_str": "12.99",
                "stex_tp": "KRX",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()

    # post 메서드는 토큰 요청용
    client_mock.post.return_value = token_response

    # request 메서드는 API 요청용
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.trade_execution_information_request_ka10003("005930")

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["cntr_infr"]) == 3

    # 첫 번째 체결 데이터 검증
    first_trade = result["cntr_infr"][0]
    assert first_trade["tm"] == "130429"
    assert first_trade["cur_prc"] == "+53500"
    assert first_trade["cntr_trde_qty"] == "1010"
    assert first_trade["stex_tp"] == "KRX"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    assert call_args[1]["json"] == {"stk_cd": "005930"}

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10003"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_credit_trading_trend_request_success_ka10013(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "crd_trend": [
            {
                "dt": "20241101",
                "cur_prc": "65100",
                "pred_pre": "0",
                "trde_qty": "12345678",
                "lend_bal": "1000",
                "lend_amt": "65100000",
                "sbor_bal": "500",
                "sbor_amt": "32550000",
            },
            {
                "dt": "20241031",
                "cur_prc": "65100",
                "pred_pre": "0",
                "trde_qty": "9876543",
                "lend_bal": "950",
                "lend_amt": "61845000",
                "sbor_bal": "480",
                "sbor_amt": "31248000",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()

    # post 메서드는 토큰 요청용
    client_mock.post.return_value = token_response

    # request 메서드는 API 요청용
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # 필요한 모든 인자를 전달하도록 수정
    test_date = "20241104"
    test_query_type = "1"

    # Act
    result = kiwoom_api.credit_trading_trend_request_ka10013(
        "005930", test_date, test_query_type
    )

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["crd_trend"]) == 2

    # 데이터 검증
    first_trend = result["crd_trend"][0]
    assert first_trend["dt"] == "20241101"
    assert first_trend["cur_prc"] == "65100"
    assert first_trend["lend_bal"] == "1000"
    assert first_trend["sbor_bal"] == "500"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    # 올바른 파라미터 확인
    assert call_args[1]["json"] == {
        "stk_cd": "005930",
        "dt": test_date,
        "qry_tp": test_query_type,
    }

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10013"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_daily_transaction_details_request_ka10015(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "daly_trde_dtl": [
            {
                "dt": "20241105",
                "close_pric": "135300",
                "pred_pre_sig": "0",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "trde_qty": "0",
                "trde_prica": "0",
                "bf_mkrt_trde_qty": "",
                "opmr_trde_qty": "",
                "af_mkrt_trde_qty": "",
                "for_netprps": "",
                "orgn_netprps": "",
                "ind_netprps": "",
                "crd_remn_rt": "",
            },
            {
                "dt": "20241104",
                "close_pric": "135300",
                "pred_pre_sig": "2",
                "pred_pre": "400",
                "flu_rt": "0.30",
                "trde_qty": "12345678",
                "trde_prica": "1670592630400",
                "bf_mkrt_trde_qty": "123456",
                "opmr_trde_qty": "12000000",
                "af_mkrt_trde_qty": "222222",
                "for_netprps": "-500000",
                "orgn_netprps": "+1000000",
                "ind_netprps": "-500000",
                "crd_remn_rt": "1.25",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.daily_transaction_details_request_ka10015("005930", "20241101")

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["daly_trde_dtl"]) == 2

    # 데이터 검증
    first_detail = result["daly_trde_dtl"][0]
    assert first_detail["dt"] == "20241105"
    assert first_detail["close_pric"] == "135300"
    assert first_detail["flu_rt"] == "0.00"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    assert call_args[1]["json"] == {"stk_cd": "005930", "strt_dt": "20241101"}

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10015"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_reported_low_price_request_ka10016(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "ntl_pric": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "334",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "trde_qty": "3",
                "pred_trde_qty_pre_rt": "-0.00",
                "sel_bid": "0",
                "buy_bid": "0",
                "high_pric": "334",
                "low_pric": "320",
            },
            {
                "stk_cd": "000660",
                "stk_nm": "SK하이닉스",
                "cur_prc": "186000",
                "pred_pre_sig": "2",
                "pred_pre": "1000",
                "flu_rt": "0.54",
                "trde_qty": "2345678",
                "pred_trde_qty_pre_rt": "120.45",
                "sel_bid": "186000",
                "buy_bid": "185900",
                "high_pric": "187500",
                "low_pric": "185000",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.reported_low_price_request_ka10016(
        market_type="001",
        new_high_low_type="1",
        high_low_close_type="1",
        stock_condition="0",
        trade_qty_type="00000",
        credit_condition="0",
        include_up_down_limit="0",
        period="5",
        exchange_type="1",
    )

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["ntl_pric"]) == 2

    # 데이터 검증
    first_price = result["ntl_pric"][0]
    assert first_price["stk_cd"] == "005930"
    assert first_price["stk_nm"] == "삼성전자"
    assert first_price["cur_prc"] == "334"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    expected_json = {
        "mrkt_tp": "001",
        "ntl_tp": "1",
        "high_low_close_tp": "1",
        "stk_cnd": "0",
        "trde_qty_tp": "00000",
        "crd_cnd": "0",
        "updown_incls": "0",
        "dt": "5",
        "stex_tp": "1",
    }
    assert call_args[1]["json"] == expected_json

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10016"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_upper_lower_limit_price_request_ka10017(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "updown_pric": [
            {
                "stk_cd": "005930",
                "stk_infr": "",
                "stk_nm": "삼성전자",
                "cur_prc": "+235500",
                "pred_pre_sig": "1",
                "pred_pre": "+54200",
                "flu_rt": "+29.90",
                "trde_qty": "0",
                "pred_trde_qty": "96197",
                "sel_req": "0",
                "sel_bid": "0",
                "buy_bid": "+235500",
                "buy_req": "4",
                "cnt": "1",
            },
            {
                "stk_cd": "000660",
                "stk_infr": "",
                "stk_nm": "SK하이닉스",
                "cur_prc": "+186500",
                "pred_pre_sig": "1",
                "pred_pre": "+43000",
                "flu_rt": "+29.95",
                "trde_qty": "0",
                "pred_trde_qty": "65432",
                "sel_req": "0",
                "sel_bid": "0",
                "buy_bid": "+186500",
                "buy_req": "10",
                "cnt": "2",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.upper_lower_limit_price_request_ka10017(
        market_type="001",
        updown_type="1",
        sort_type="3",
        stock_condition="0",
        trade_qty_type="00010",
        credit_condition="0",
        trade_gold_type="0",
        exchange_type="1",
    )

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["updown_pric"]) == 2

    # 데이터 검증
    first_limit = result["updown_pric"][0]
    assert first_limit["stk_cd"] == "005930"
    assert first_limit["stk_nm"] == "삼성전자"
    assert first_limit["cur_prc"] == "+235500"
    assert first_limit["flu_rt"] == "+29.90"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    expected_json = {
        "mrkt_tp": "001",
        "updown_tp": "1",
        "sort_tp": "3",
        "stk_cnd": "0",
        "trde_qty_tp": "00010",
        "crd_cnd": "0",
        "trde_gold_tp": "0",
        "stex_tp": "1",
    }
    assert call_args[1]["json"] == expected_json

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10017"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_near_high_low_price_request_ka10018(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "high_low_pric_alacc": [
            {
                "stk_cd": "004930",
                "stk_nm": "삼성전자",
                "cur_prc": "334",
                "pred_pre_sig": "0",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "trde_qty": "3",
                "sel_bid": "0",
                "buy_bid": "0",
                "tdy_high_pric": "334",
                "tdy_low_pric": "334",
            },
            {
                "stk_cd": "004930",
                "stk_nm": "삼성전자",
                "cur_prc": "+7470",
                "pred_pre_sig": "2",
                "pred_pre": "+90",
                "flu_rt": "+1.22",
                "trde_qty": "2",
                "sel_bid": "0",
                "buy_bid": "-7320",
                "tdy_high_pric": "+7470",
                "tdy_low_pric": "+7470",
            },
            {
                "stk_cd": "008370",
                "stk_nm": "원풍",
                "cur_prc": "+4970",
                "pred_pre_sig": "0",
                "pred_pre": "+15",
                "flu_rt": "+0.30",
                "trde_qty": "500",
                "sel_bid": "0",
                "buy_bid": "0",
                "tdy_high_pric": "+4970",
                "tdy_low_pric": "+4970",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.near_high_low_price_request_ka10018(
        high_low_type="1",
        proximity_rate="05",
        market_type="000",
        trade_qty_type="0000",
        stock_condition="0",
        credit_condition="0",
        exchange_type="1",
    )

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["high_low_pric_alacc"]) == 3

    # 데이터 검증
    first_item = result["high_low_pric_alacc"][0]
    assert first_item["stk_cd"] == "004930"
    assert first_item["stk_nm"] == "삼성전자"
    assert first_item["cur_prc"] == "334"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    expected_json = {
        "high_low_tp": "1",
        "alacc_rt": "05",
        "mrkt_tp": "000",
        "trde_qty_tp": "0000",
        "stk_cnd": "0",
        "crd_cnd": "0",
        "stex_tp": "1",
    }
    assert call_args[1]["json"] == expected_json

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10018"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_rapid_price_change_request_ka10019(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "pric_jmpflu": [
            {
                "stk_cd": "005930",
                "stk_cls": "",
                "stk_nm": "삼성전자",
                "pred_pre_sig": "2",
                "pred_pre": "+300",
                "flu_rt": "+0.57",
                "base_pric": "51600",
                "cur_prc": "+52700",
                "base_pre": "1100",
                "trde_qty": "2400",
                "jmp_rt": "+2.13",
            },
            {
                "stk_cd": "005930",
                "stk_cls": "",
                "stk_nm": "삼성전자",
                "pred_pre_sig": "5",
                "pred_pre": "-24200",
                "flu_rt": "-26.68",
                "base_pric": "66000",
                "cur_prc": "-66500",
                "base_pre": "500",
                "trde_qty": "577",
                "jmp_rt": "+0.76",
            },
            {
                "stk_cd": "005930",
                "stk_cls": "",
                "stk_nm": "삼성전자",
                "pred_pre_sig": "2",
                "pred_pre": "+10",
                "flu_rt": "+0.06",
                "base_pric": "16370",
                "cur_prc": "+16380",
                "base_pre": "10",
                "trde_qty": "102",
                "jmp_rt": "+0.06",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.rapid_price_change_request_ka10019(
        market_type="000",
        fluctuation_type="1",
        time_type="1",
        time="60",
        trade_qty_type="0000",
        stock_condition="0",
        credit_condition="0",
        price_condition="0",
        include_up_down_limit="1",
        exchange_type="1",
    )

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["pric_jmpflu"]) == 3

    # 데이터 검증
    first_item = result["pric_jmpflu"][0]
    assert first_item["stk_cd"] == "005930"
    assert first_item["stk_nm"] == "삼성전자"
    assert first_item["cur_prc"] == "+52700"
    assert first_item["jmp_rt"] == "+2.13"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    expected_json = {
        "mrkt_tp": "000",
        "flu_tp": "1",
        "tm_tp": "1",
        "tm": "60",
        "trde_qty_tp": "0000",
        "stk_cnd": "0",
        "crd_cnd": "0",
        "pric_cnd": "0",
        "updown_incls": "1",
        "stex_tp": "1",
    }
    assert call_args[1]["json"] == expected_json

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10019"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_trading_volume_update_request_ka10024(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "trde_qty_updt": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+74800",
                "pred_pre_sig": "1",
                "pred_pre": "+17200",
                "flu_rt": "+29.86",
                "prev_trde_qty": "243520",
                "now_trde_qty": "435771",
                "sel_bid": "0",
                "buy_bid": "+74800",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-42900",
                "pred_pre_sig": "5",
                "pred_pre": "-150",
                "flu_rt": "-0.35",
                "prev_trde_qty": "25377975",
                "now_trde_qty": "31399114",
                "sel_bid": "-42900",
                "buy_bid": "+45250",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-152000",
                "pred_pre_sig": "5",
                "pred_pre": "-100",
                "flu_rt": "-0.07",
                "prev_trde_qty": "22435675",
                "now_trde_qty": "31491771",
                "sel_bid": "-152000",
                "buy_bid": "-151900",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.trading_volume_update_request_ka10024(
        market_type="000", cycle_type="5", trade_qty_type="5", exchange_type="3"
    )

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["trde_qty_updt"]) == 3

    # 데이터 검증
    first_item = result["trde_qty_updt"][0]
    assert first_item["stk_cd"] == "005930"
    assert first_item["stk_nm"] == "삼성전자"
    assert first_item["cur_prc"] == "+74800"
    assert first_item["prev_trde_qty"] == "243520"
    assert first_item["now_trde_qty"] == "435771"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    expected_json = {
        "mrkt_tp": "000",
        "cycle_tp": "5",
        "trde_qty_tp": "5",
        "stex_tp": "3",
    }
    assert call_args[1]["json"] == expected_json

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10024"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_supply_concentration_request_ka10025(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "prps_cnctr": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "30000",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "now_trde_qty": "0",
                "pric_strt": "31350",
                "pric_end": "31799",
                "prps_qty": "4",
                "prps_rt": "+50.00",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "30000",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "now_trde_qty": "0",
                "pric_strt": "32700",
                "pric_end": "33149",
                "prps_qty": "4",
                "prps_rt": "+50.00",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "109",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "now_trde_qty": "1",
                "pric_strt": "109",
                "pric_end": "326",
                "prps_qty": "8",
                "prps_rt": "+50.00",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.supply_concentration_request_ka10025(
        market_type="000",
        supply_concentration_rate="50",
        current_price_entry="0",
        supply_count="10",
        cycle_type="50",
        exchange_type="3",
    )

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["prps_cnctr"]) == 3

    # 데이터 검증
    first_item = result["prps_cnctr"][0]
    assert first_item["stk_cd"] == "005930"
    assert first_item["stk_nm"] == "삼성전자"
    assert first_item["cur_prc"] == "30000"
    assert first_item["pric_strt"] == "31350"
    assert first_item["pric_end"] == "31799"
    assert first_item["prps_rt"] == "+50.00"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    expected_json = {
        "mrkt_tp": "000",
        "prps_cnctr_rt": "50",
        "cur_prc_entry": "0",
        "prpscnt": "10",
        "cycle_tp": "50",
        "stex_tp": "3",
    }
    assert call_args[1]["json"] == expected_json

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10025"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_high_low_per_request_ka10026(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "high_low_per": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "per": "0.44",
                "cur_prc": "4930",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "now_trde_qty": "0",
                "sel_bid": "0",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "per": "0.54",
                "cur_prc": "5980",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "now_trde_qty": "0",
                "sel_bid": "0",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "per": "0.71",
                "cur_prc": "3445",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "now_trde_qty": "0",
                "sel_bid": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.high_low_per_request_ka10026(per_type="1", exchange_type="3")

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["high_low_per"]) == 3

    # 데이터 검증
    first_item = result["high_low_per"][0]
    assert first_item["stk_cd"] == "005930"
    assert first_item["stk_nm"] == "삼성전자"
    assert first_item["per"] == "0.44"
    assert first_item["cur_prc"] == "4930"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    expected_json = {"pertp": "1", "stex_tp": "3"}
    assert call_args[1]["json"] == expected_json

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10026"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_rate_of_change_compared_to_opening_price_request_ka10028(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "open_pric_pre_flu_rt": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+74800",
                "pred_pre_sig": "1",
                "pred_pre": "+17200",
                "flu_rt": "+29.86",
                "open_pric": "+65000",
                "high_pric": "+74800",
                "low_pric": "-57000",
                "open_pric_pre": "+15.08",
                "now_trde_qty": "448203",
                "cntr_str": "346.54",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-200000",
                "pred_pre_sig": "5",
                "pred_pre": "-15000",
                "flu_rt": "-6.98",
                "open_pric": "-180000",
                "high_pric": "215000",
                "low_pric": "-180000",
                "open_pric_pre": "+11.11",
                "now_trde_qty": "619",
                "cntr_str": "385.07",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+200000",
                "pred_pre_sig": "2",
                "pred_pre": "+15600",
                "flu_rt": "+8.46",
                "open_pric": "184400",
                "high_pric": "+200000",
                "low_pric": "-183500",
                "open_pric_pre": "+8.46",
                "now_trde_qty": "143",
                "cntr_str": "500.00",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.rate_of_change_compared_to_opening_price_request_ka10028(
        sort_type="1",
        trade_qty_condition="0000",
        market_type="000",
        include_up_down_limit="1",
        stock_condition="0",
        credit_condition="0",
        trade_price_condition="0",
        fluctuation_condition="1",
        exchange_type="3",
    )

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["open_pric_pre_flu_rt"]) == 3

    # 데이터 검증
    first_item = result["open_pric_pre_flu_rt"][0]
    assert first_item["stk_cd"] == "005930"
    assert first_item["stk_nm"] == "삼성전자"
    assert first_item["cur_prc"] == "+74800"
    assert first_item["open_pric"] == "+65000"
    assert first_item["open_pric_pre"] == "+15.08"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    expected_json = {
        "sort_tp": "1",
        "trde_qty_cnd": "0000",
        "mrkt_tp": "000",
        "updown_incls": "1",
        "stk_cnd": "0",
        "crd_cnd": "0",
        "trde_prica_cnd": "0",
        "flu_cnd": "1",
        "stex_tp": "3",
    }
    assert call_args[1]["json"] == expected_json

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10028"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_trading_agent_supply_demand_analysis_request_ka10043(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "trde_ori_prps_anly": [
            {
                "dt": "20241105",
                "close_pric": "135300",
                "pre_sig": "2",
                "pred_pre": "+1700",
                "sel_qty": "43",
                "buy_qty": "1090",
                "netprps_qty": "1047",
                "trde_qty_sum": "1133",
                "trde_wght": "+1317.44",
            },
            {
                "dt": "20241107",
                "close_pric": "133600",
                "pre_sig": "3",
                "pred_pre": "0",
                "sel_qty": "0",
                "buy_qty": "0",
                "netprps_qty": "0",
                "trde_qty_sum": "0",
                "trde_wght": "0.00",
            },
            {
                "dt": "20241106",
                "close_pric": "132500",
                "pre_sig": "5",
                "pred_pre": "--1100",
                "sel_qty": "117",
                "buy_qty": "3459",
                "netprps_qty": "3342",
                "trde_qty_sum": "3576",
                "trde_wght": "+4158.14",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.trading_agent_supply_demand_analysis_request_ka10043(
        stock_code="005930",
        start_date="20241031",
        end_date="20241107",
        query_date_type="0",
        point_type="0",
        date="5",
        sort_base="1",
        member_code="36",
        exchange_type="3",
    )

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["trde_ori_prps_anly"]) == 3

    # 데이터 검증
    first_item = result["trde_ori_prps_anly"][0]
    assert first_item["dt"] == "20241105"
    assert first_item["close_pric"] == "135300"
    assert first_item["netprps_qty"] == "1047"
    assert first_item["trde_wght"] == "+1317.44"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    expected_json = {
        "stk_cd": "005930",
        "strt_dt": "20241031",
        "end_dt": "20241107",
        "qry_dt_tp": "0",
        "pot_tp": "0",
        "dt": "5",
        "sort_base": "1",
        "mmcm_cd": "36",
        "stex_tp": "3",
    }
    assert call_args[1]["json"] == expected_json

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10043"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_trading_agent_instant_trading_volume_request_ka10052(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "trde_ori_mont_trde_qty": [
            {
                "tm": "161437",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "trde_ori_nm": "다이와",
                "tp": "-매도",
                "mont_trde_qty": "-399928",
                "acc_netprps": "-1073004",
                "cur_prc": "+57700",
                "pred_pre_sig": "2",
                "pred_pre": "400",
                "flu_rt": "+0.70",
            },
            {
                "tm": "161423",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "trde_ori_nm": "다이와",
                "tp": "-매도",
                "mont_trde_qty": "-100000",
                "acc_netprps": "-673076",
                "cur_prc": "+57700",
                "pred_pre_sig": "2",
                "pred_pre": "400",
                "flu_rt": "+0.70",
            },
            {
                "tm": "161417",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "trde_ori_nm": "다이와",
                "tp": "-매도",
                "mont_trde_qty": "-100000",
                "acc_netprps": "-573076",
                "cur_prc": "+57700",
                "pred_pre_sig": "2",
                "pred_pre": "400",
                "flu_rt": "+0.70",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.trading_agent_instant_trading_volume_request_ka10052(
        member_code="888",
        stock_code="",
        market_type="0",
        quantity_type="0",
        price_type="0",
        exchange_type="3",
    )

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["trde_ori_mont_trde_qty"]) == 3

    # 데이터 검증
    first_item = result["trde_ori_mont_trde_qty"][0]
    assert first_item["tm"] == "161437"
    assert first_item["stk_cd"] == "005930"
    assert first_item["stk_nm"] == "삼성전자"
    assert first_item["trde_ori_nm"] == "다이와"
    assert first_item["mont_trde_qty"] == "-399928"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    expected_json = {
        "mmcm_cd": "888",
        "stk_cd": "",
        "mrkt_tp": "0",
        "qty_tp": "0",
        "pric_tp": "0",
        "stex_tp": "3",
    }
    assert call_args[1]["json"] == expected_json

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10052"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_volatility_mitigation_device_triggered_stocks_request_ka10054(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "motn_stk": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "acc_trde_qty": "1105968",
                "motn_pric": "67000",
                "dynm_dispty_rt": "+9.30",
                "trde_cntr_proc_time": "172311",
                "virelis_time": "172511",
                "viaplc_tp": "동적",
                "dynm_stdpc": "61300",
                "static_stdpc": "0",
                "static_dispty_rt": "0.00",
                "open_pric_pre_flu_rt": "+16.93",
                "vimotn_cnt": "23",
                "stex_tp": "NXT",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "acc_trde_qty": "1105968",
                "motn_pric": "65000",
                "dynm_dispty_rt": "-3.13",
                "trde_cntr_proc_time": "170120",
                "virelis_time": "170320",
                "viaplc_tp": "동적",
                "dynm_stdpc": "67100",
                "static_stdpc": "0",
                "static_dispty_rt": "0.00",
                "open_pric_pre_flu_rt": "+13.44",
                "vimotn_cnt": "22",
                "stex_tp": "NXT",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.volatility_mitigation_device_triggered_stocks_request_ka10054(
        market_type="000",
        before_market_type="0",
        stock_code="",
        motion_type="0",
        skip_stocks="000000000",
        trade_qty_type="0",
        min_trade_qty="0",
        max_trade_qty="0",
        trade_price_type="0",
        min_trade_price="0",
        max_trade_price="0",
        motion_direction="0",
        exchange_type="3",
    )

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["motn_stk"]) == 2

    # 데이터 검증
    first_item = result["motn_stk"][0]
    assert first_item["stk_cd"] == "005930"
    assert first_item["stk_nm"] == "삼성전자"
    assert first_item["acc_trde_qty"] == "1105968"
    assert first_item["motn_pric"] == "67000"
    assert first_item["viaplc_tp"] == "동적"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    expected_json = {
        "mrkt_tp": "000",
        "bf_mkrt_tp": "0",
        "stk_cd": "",
        "motn_tp": "0",
        "skip_stk": "000000000",
        "trde_qty_tp": "0",
        "min_trde_qty": "0",
        "max_trde_qty": "0",
        "trde_prica_tp": "0",
        "min_trde_prica": "0",
        "max_trde_prica": "0",
        "motn_drc": "0",
        "stex_tp": "3",
    }
    assert call_args[1]["json"] == expected_json

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10054"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_today_vs_previous_day_execution_volume_request_ka10055(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "tdy_pred_cntr_qty": [
            {
                "cntr_tm": "171945",
                "cntr_pric": "+74800",
                "pred_pre_sig": "1",
                "pred_pre": "+17200",
                "flu_rt": "+29.86",
                "cntr_qty": "-1793",
                "acc_trde_qty": "446203",
                "acc_trde_prica": "33225",
            },
            {
                "cntr_tm": "154626",
                "cntr_pric": "+74800",
                "pred_pre_sig": "1",
                "pred_pre": "+17200",
                "flu_rt": "+29.86",
                "cntr_qty": "-1",
                "acc_trde_qty": "444401",
                "acc_trde_prica": "33090",
            },
            {
                "cntr_tm": "154357",
                "cntr_pric": "+74800",
                "pred_pre_sig": "1",
                "pred_pre": "+17200",
                "flu_rt": "+29.86",
                "cntr_qty": "-100",
                "acc_trde_qty": "444399",
                "acc_trde_prica": "33090",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.today_vs_previous_day_execution_volume_request_ka10055(
        stock_code="005930", today_previous="2"
    )

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["tdy_pred_cntr_qty"]) == 3

    # 데이터 검증
    first_item = result["tdy_pred_cntr_qty"][0]
    assert first_item["cntr_tm"] == "171945"
    assert first_item["cntr_pric"] == "+74800"
    assert first_item["pred_pre"] == "+17200"
    assert first_item["cntr_qty"] == "-1793"
    assert first_item["acc_trde_qty"] == "446203"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    expected_json = {"stk_cd": "005930", "tdy_pred": "2"}
    assert call_args[1]["json"] == expected_json

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10055"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_daily_trading_stocks_by_investor_type_request_ka10058(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "invsr_daly_trde_stk": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "netslmt_qty": "+4464",
                "netslmt_amt": "+25467",
                "prsm_avg_pric": "57056",
                "cur_prc": "+61300",
                "pre_sig": "2",
                "pred_pre": "+4000",
                "avg_pric_pre": "+4244",
                "pre_rt": "+7.43",
                "dt_trde_qty": "1554171",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "netslmt_qty": "+12",
                "netslmt_amt": "+106",
                "prsm_avg_pric": "86658",
                "cur_prc": "+100200",
                "pre_sig": "2",
                "pred_pre": "+5200",
                "avg_pric_pre": "+13542",
                "pre_rt": "+15.62",
                "dt_trde_qty": "12868",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "netslmt_qty": "+46",
                "netslmt_amt": "+75",
                "prsm_avg_pric": "16320",
                "cur_prc": "15985",
                "pre_sig": "3",
                "pred_pre": "0",
                "avg_pric_pre": "--335",
                "pre_rt": "-2.05",
                "dt_trde_qty": "4770",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.daily_trading_stocks_by_investor_type_request_ka10058(
        start_date="20241106",
        end_date="20241107",
        trade_type="2",
        market_type="101",
        investor_type="8000",
        exchange_type="3",
    )

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["invsr_daly_trde_stk"]) == 3

    # 데이터 검증
    first_item = result["invsr_daly_trde_stk"][0]
    assert first_item["stk_cd"] == "005930"
    assert first_item["stk_nm"] == "삼성전자"
    assert first_item["netslmt_qty"] == "+4464"
    assert first_item["netslmt_amt"] == "+25467"
    assert first_item["cur_prc"] == "+61300"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    expected_json = {
        "strt_dt": "20241106",
        "end_dt": "20241107",
        "trde_tp": "2",
        "mrkt_tp": "101",
        "invsr_tp": "8000",
        "stex_tp": "3",
    }
    assert call_args[1]["json"] == expected_json

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10058"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_stock_data_by_investor_institution_request_ka10059(
    kiwoom_api: KiwoomAPI, mocker: MockerFixture
) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0,
    }

    # API 응답 모킹
    api_response = mocker.Mock()
    api_response.json.return_value = {
        "stk_invsr_orgn": [
            {
                "dt": "20241107",
                "cur_prc": "+61300",
                "pre_sig": "2",
                "pred_pre": "+4000",
                "flu_rt": "+698",
                "acc_trde_qty": "1105968",
                "acc_trde_prica": "64215",
                "ind_invsr": "1584",
                "frgnr_invsr": "-61779",
                "orgn": "60195",
                "fnnc_invt": "25514",
                "insrnc": "0",
                "invtrt": "0",
                "etc_fnnc": "34619",
                "bank": "4",
                "penfnd_etc": "-1",
                "samo_fund": "58",
                "natn": "0",
                "etc_corp": "0",
                "natfor": "1",
            },
            {
                "dt": "20241106",
                "cur_prc": "+74800",
                "pre_sig": "1",
                "pred_pre": "+17200",
                "flu_rt": "+2986",
                "acc_trde_qty": "448203",
                "acc_trde_prica": "33340",
                "ind_invsr": "-639",
                "frgnr_invsr": "-7",
                "orgn": "646",
                "fnnc_invt": "-47",
                "insrnc": "15",
                "invtrt": "-2",
                "etc_fnnc": "730",
                "bank": "-51",
                "penfnd_etc": "1",
                "samo_fund": "0",
                "natn": "0",
                "etc_corp": "0",
                "natfor": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    # httpx Client 모킹
    client_mock = mocker.Mock()
    client_mock.post.return_value = token_response
    client_mock.request.return_value = api_response

    # 모킹된 클라이언트를 KiwoomAPI 인스턴스에 주입
    mocker.patch("httpx.Client", return_value=client_mock)
    kiwoom_api.client = client_mock

    # Act
    result = kiwoom_api.stock_data_by_investor_institution_request_ka10059(
        date="20241107",
        stock_code="005930",
        amount_quantity_type="1",
        trade_type="0",
        unit_type="1000",
    )

    # Assert - 응답 결과 검증
    assert result["return_code"] == 0
    assert len(result["stk_invsr_orgn"]) == 2

    # 데이터 검증
    first_item = result["stk_invsr_orgn"][0]
    assert first_item["dt"] == "20241107"
    assert first_item["cur_prc"] == "+61300"
    assert first_item["flu_rt"] == "+698"
    assert first_item["ind_invsr"] == "1584"
    assert first_item["frgnr_invsr"] == "-61779"
    assert first_item["orgn"] == "60195"

    # HTTP 요청 파라미터 검증
    call_args = client_mock.request.call_args
    assert call_args[1]["method"] == "POST"
    assert call_args[1]["url"] == f"{kiwoom_api.base_url}/api/dostk/stkinfo"
    expected_json = {
        "dt": "20241107",
        "stk_cd": "005930",
        "amt_qty_tp": "1",
        "trde_tp": "0",
        "unit_tp": "1000",
    }
    assert call_args[1]["json"] == expected_json

    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10059"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"
