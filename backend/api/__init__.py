"""
JobConnect API module. Uses FastAPI.
"""

# Relevant for compatibility with CLI operations
# that interact with Django database models

import os
import time
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JobConnect.settings")
import django

django.setup()

from api.v1 import router as v1_router
from JobConnect.settings import (
    STATIC_URL,
    MEDIA_URL,
    STATIC_ROOT,
    MEDIA_ROOT,
    FRONTED_DIR,
)

api_module_path = Path(__file__).parent
api_prefix = "/api"

app = FastAPI(
    title="JobConnect API",
    version=api_module_path.joinpath("VERSION").read_text().strip(),
    description=api_module_path.joinpath("README.md").read_text(),
    license_info={
        "name": "MIT License",
        "url": "https://raw.githubusercontent.com/Simatwa/JobConnect/refs/heads/main/LICENSE",
    },
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)

# Mount static & media files
app.mount(STATIC_URL[:-1], StaticFiles(directory=STATIC_ROOT), name="static")
app.mount(MEDIA_URL[:-1], StaticFiles(directory=MEDIA_ROOT), name="media")

from django.core.handlers.wsgi import WSGIHandler

from fastapi.middleware.wsgi import WSGIMiddleware

app.mount("/d", app=WSGIMiddleware(WSGIHandler()), name="django")

# Include API router
app.include_router(v1_router, prefix=api_prefix)

if FRONTED_DIR:
    # let's serve the frontend dir
    app.mount("/", StaticFiles(directory=FRONTED_DIR, html=True))
