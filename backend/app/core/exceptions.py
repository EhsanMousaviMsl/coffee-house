from http import HTTPStatus


class AppException(Exception):
    status_code: int = HTTPStatus.BAD_REQUEST
    error_code: str = "APPLICATION_ERROR"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class CategoryNotFoundError(AppException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "CATEGORY_NOT_FOUND"

    def __init__(self, category_id: int):
        super().__init__(
            f"Category with id {category_id} not found"
        )

class ProductNotFoundError(AppException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "PRODUCT_NOT_FOUND"

    def __init__(self, product_id: int):
        super().__init__(
            f"Product with id {product_id} not found"
        )