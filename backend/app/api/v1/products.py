from fastapi import APIRouter, Depends

from app.services.product_service import ProductService
from app.dependencies.products import get_product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("/")
def get_products(
    service: ProductService = Depends(get_product_service),
):
    return service.get_all_products()