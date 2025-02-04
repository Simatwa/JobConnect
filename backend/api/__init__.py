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
from JobConnect.settings import STATIC_ROOT

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

# CORS Middleware - Uncommented to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_ROOT))

# Include API router
app.include_router(v1_router, prefix=api_prefix)
