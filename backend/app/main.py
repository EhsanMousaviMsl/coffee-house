from fastapi import FastAPI, Request
from app.core.config import settings
from app import models
from app.api.v1.products import router as product_router
from fastapi.responses import JSONResponse
from app.core.exceptions import CategoryNotFoundError


app = FastAPI(title=settings.app_name, version=settings.app_version)

app.include_router(
    product_router,
    prefix="/api/v1",
)

@app.exception_handler(CategoryNotFoundError)
async def category_not_found_handler(
    request: Request,
    exc: CategoryNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
        },
    )