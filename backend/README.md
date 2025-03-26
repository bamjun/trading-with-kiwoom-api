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