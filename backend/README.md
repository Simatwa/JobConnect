The whole idea is to let [FastAPI](https://fastapi.tiangolo.com) serve client requests while Django to handle models administration.

## Installation

```shell
pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python -m fastapi run
```

