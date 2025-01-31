The whole idea is to let [FastAPI](https://fastapi.tiangolo.com) serve client requests while Django to handle models administration.

## Installation & Setup

```shell
pip install -r requirements.txt

python manage.py makemigrations users jobs

python manage.py migrate

python manage.py collectstatic

python -m api fake all

python manage.py createsuperuser
```

> [!TIP]
> Use make command to accomplish the same: `$ make`
> Username : ```developer```
> Password : ```development```

## Start Server

```shell
python -m fastapi run
```

## Endpoints

| Endpoint | Purpose |
|----------|----------|
| `/api/docs` | Docs |
| `/api/redoc` | Redoc |
| `/admin` | Admin |
