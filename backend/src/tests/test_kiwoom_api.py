import pytest
from a_stocks._utils.kiwoom_api import KiwoomAPI

@pytest.fixture
def kiwoom_api():
    return KiwoomAPI()

def test_basic_stock_information_request_success(kiwoom_api, mocker):
    # Arrange
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "stk_cd": "005930",
        "stk_nm": "삼성전자",
        "setl_mm": "12",
        "fav": "5000",
        "cap": "1311",
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다"
    }
    mock_client = mocker.patch('httpx.Client')
    mock_client.return_value.request.return_value = mock_response

    # Act
    result = kiwoom_api.basic_stock_information_request("005930")
    print(result)

    # Assert
    assert result["stk_cd"] == "005930"
    assert result["stk_nm"] == "삼성전자"
    assert result["return_code"] == 0
    assert result["return_msg"] == "정상적으로 처리되었습니다"
