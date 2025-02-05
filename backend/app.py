### Django here

# import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JobConnect.settings")

# import django

# django.setup()

# from django.core.handlers.wsgi import WSGIHandler

from api import app

# from fastapi.middleware.wsgi import WSGIMiddleware

# app.mount("/", app=WSGIMiddleware(WSGIHandler()), name="django")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
