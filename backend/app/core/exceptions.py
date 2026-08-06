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

class CategoryAlreadyExistsError(AppException):
    status_code = HTTPStatus.CONFLICT
    error_code = "CATEGORY_ALREADY_EXISTS"

    def __init__(self, name: str):
        super().__init__(
            f"Category '{name}' already exists"
        )


class CategoryHasProductsError(AppException):
    status_code = HTTPStatus.CONFLICT
    error_code = "CATEGORY_HAS_PRODUCTS"

    def __init__(self, category_id: int):
        super().__init__(
            f"Cannot delete category {category_id} because it has products"
        )

class ProductUnavailableError(AppException):
    status_code = HTTPStatus.CONFLICT
    error_code = "PRODUCT_UNAVAILABLE"

    def __init__(self, product_id: int):
        super().__init__(
            f"Product with id {product_id} is not available"
        )


class InsufficientInventoryError(AppException):
    status_code = HTTPStatus.CONFLICT
    error_code = "INSUFFICIENT_INVENTORY"

    def __init__(
        self,
        product_id: int,
        requested: int,
        available: int,
    ):
        super().__init__(
            f"Product with id {product_id} has insufficient inventory: "
            f"requested {requested}, available {available}"
        )

class OrderNotFoundError(AppException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "ORDER_NOT_FOUND"

    def __init__(self, order_id: int):
        super().__init__(
            f"Order with id {order_id} not found"
        )