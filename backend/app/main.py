from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.exceptions import AppException
from app.api.v1.api import api_router
from app import models


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


origins = [
    origin.strip()
    for origin in settings.cors_origins.split(",")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    api_router,
    prefix="/api/v1",
)


@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
        },
    )