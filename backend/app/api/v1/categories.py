from fastapi import APIRouter, Depends, status

from app.dependencies.categories import get_category_service
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category_service import CategoryService


router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

@router.get(
    "/",
    response_model=list[CategoryResponse],
)
def get_categories(
    service: CategoryService = Depends(
        get_category_service
    ),
):
    return service.get_all_categories()

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    service: CategoryService = Depends(
        get_category_service
    ),
):
    return service.get_category_by_id(category_id)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    data: CategoryCreate,
    service: CategoryService = Depends(
        get_category_service
    ),
):
    return service.create_category(data)

@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    service: CategoryService = Depends(
        get_category_service
    ),
):
    return service.update_category(
        category_id,
        data,
    )

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: int,
    service: CategoryService = Depends(
        get_category_service
    ),
):
    service.delete_category(category_id)