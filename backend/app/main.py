from fastapi import FastAPI, Request
from app.core.config import settings
from app import models
from app.api.v1.products import router as product_router
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException, CategoryNotFoundError


app = FastAPI(title=settings.app_name, version=settings.app_version)

app.include_router(
    product_router,
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