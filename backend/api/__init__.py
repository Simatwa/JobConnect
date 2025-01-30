""" 
JobConnect API module. Uses FastAPI.
"""

# Relevant for compatibility with CLI operations
# that interacts with django database models

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JobConnect.settings")
import django

django.setup()


from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from api.v1 import router as v1_router
from JobConnect.settings import STATIC_ROOT
import time


<<<<<<< HEAD

=======
>>>>>>> ed72b6b67674b771c8f4840a3186ff97d72b9a0d
api_module_path = Path(__file__).parent

api_prefix = "/api"

app = FastAPI(
    title="JobConnect API",
    version=api_module_path.joinpath("VERSION").read_text(),
    description=api_module_path.joinpath("README").read_text(),
    license_info={
        "name": "MIT License",
        "url": "https://raw.githubusercontent.com/Simatwa/JobConnect/refs/heads/main/LICENSE",
    },
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)




@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


<<<<<<< HEAD

=======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
>>>>>>> ed72b6b67674b771c8f4840a3186ff97d72b9a0d

app.mount("/static", StaticFiles(directory=STATIC_ROOT))

app.include_router(v1_router, prefix=api_prefix)
