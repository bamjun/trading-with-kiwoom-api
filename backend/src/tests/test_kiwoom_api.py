from datetime import datetime, timedelta

import pytest
from pytest_mock import MockerFixture
from a_stocks._utils.kiwoom_api import KiwoomAPI


@pytest.fixture
def kiwoom_api() -> KiwoomAPI:
    return KiwoomAPI()


def test_basic_stock_information_request_success_ka10001(kiwoom_api: KiwoomAPI, mocker: MockerFixture) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0
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


def test_stock_trading_agent_request_success_ka10002(kiwoom_api: KiwoomAPI, mocker: MockerFixture) -> None:
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


def test_trade_execution_information_request_success_ka10003(kiwoom_api: KiwoomAPI, mocker: MockerFixture) -> None:
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


def test_credit_trading_trend_request_success_ka10013(kiwoom_api: KiwoomAPI, mocker: MockerFixture) -> None:
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


def test_daily_transaction_details_request_ka10015(kiwoom_api: KiwoomAPI, mocker: MockerFixture) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0
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
                "crd_remn_rt": ""
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
                "crd_remn_rt": "1.25"
            }
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다"
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


def test_reported_low_price_request_ka10016(kiwoom_api: KiwoomAPI, mocker: MockerFixture) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0
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
                "low_pric": "320"
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
                "low_pric": "185000"
            }
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다"
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
        exchange_type="1"
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
        "stex_tp": "1"
    }
    assert call_args[1]["json"] == expected_json
    
    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10016"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"


def test_upper_lower_limit_price_request_ka10017(kiwoom_api: KiwoomAPI, mocker: MockerFixture) -> None:
    # 토큰 발급 응답 모킹
    token_response = mocker.Mock()
    token_response.json.return_value = {
        "token": "test_access_token",
        "expires_dt": (datetime.now() + timedelta(hours=1)).strftime("%Y%m%d%H%M%S"),
        "return_code": 0
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
                "cnt": "1"
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
                "cnt": "2"
            }
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다"
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
        exchange_type="1"
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
        "stex_tp": "1"
    }
    assert call_args[1]["json"] == expected_json
    
    # 헤더 검증
    headers = call_args[1]["headers"]
    assert headers["api-id"] == "ka10017"
    assert headers["Authorization"] == "Bearer test_access_token"
    assert headers["Content-Type"] == "application/json;charset=UTF-8"

