from fastapi import APIRouter, Depends, status
from app.dependencies.products import get_product_service
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import ProductService


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get(
    "/",
    response_model=list[ProductResponse],
)
def get_products(
    service: ProductService = Depends(get_product_service),
):
    return service.get_all_products()


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    return service.create_product(data)