- os: window  
- ide: cursor  
- python pakage tool: uv  
    - install  
    [link of uv installation docs](https://docs.astral.sh/uv/#installation)
    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
- web framework : django
    - install  
    ```bash
    uv add django==4.2
    source .venv/scripts/activate
    mkdir src
    cd src
    django-admin startproject _core .
    python manage.py startapp a_stocks
    ```  



- run app with docker
    - bash command  
    ```bash
    export DB_PASSWORD="mydbpassword"
    export DB_USER="mydbuser"
    export DB_NAME="mydbname"
    export DB_HOST="mydbhost"
    export ACCESS_TOKEN_SECRET_KEY="mysecretkey"
    ```

    ```bash
    docker build --secret id=DB_PASSWORD \
             --secret id=DB_USER \
             --secret id=DB_NAME \
             --secret id=DB_HOST \
             --secret id=ACCESS_TOKEN_SECRET_KEY \
             --target=production \
             -f Dockerfile . -t django
    ```

- install django-nina
  - install  
    `./trading-with-kiwoom-api/backend/`
    ```bash
    uv add django-ninja
    ```

  - adding app to `INSTALLED_APPS` in settings.py
    `./trading-with-kiwoom-api/backend/src/_core/settings.py`
    ```python
    INSTALLED_APPS = [
      ...
      'ninja',
    ]
    ```

- install ruff(static analyzer tool), mypy(Linters)
  - install
    `./trading-with-kiwoom-api/backend/`  
    ```bash
    uv add --group dev ruff mypy django-stubs
    ```


# 스크립트
```bash
# 린팅 확인
ruff check .

# 린팅 자동 수정 (isort 기능 포함)
ruff check . --fix

# 코드 포맷팅 (black 기능 포함)
ruff format .

# lintters 실행
mypy .
```



# 환경설정
키움 REST API 에 IP 등록하기
[키움증권 IP주소등록 페이지](https://openapi.kiwoom.com/mgmt/VOpenApiRegView)


# class KiwoomAPI 테스트
```bash
cd backend/src
uv run python manage.py shell
```

### 계좌잔액 조회
```python
from a_stocks._utils.kiwoom_api import KiwoomAPI
api = KiwoomAPI()
api.get_account_balance(account_number="12345678")
```

### 기간별 실현 이익조회
```python
from a_stocks._utils.kiwoom_api import KiwoomAPI
api = KiwoomAPI()
te.get_order_history(account_number="12345678", start_date="20250301", end_date="20250331")
```