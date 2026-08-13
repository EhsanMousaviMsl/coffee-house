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

class OrderAlreadyCancelledError(AppException):
    status_code = HTTPStatus.CONFLICT
    error_code = "ORDER_ALREADY_CANCELLED"

    def __init__(self, order_id: int):
        super().__init__(
            f"Order {order_id} is already cancelled"
        )

class OrderCannotBeCancelledError(AppException):
    status_code = HTTPStatus.CONFLICT
    error_code = "ORDER_CANNOT_BE_CANCELLED"

    def __init__(
        self,
        order_id: int,
        status: str,
    ):
        super().__init__(
            f"Order {order_id} cannot be cancelled "
            f"because its status is {status}"
        )

class OrderCannotBeConfirmedError(AppException):
    status_code = HTTPStatus.CONFLICT
    error_code = "ORDER_CANNOT_BE_CONFIRMED"

    def __init__(
        self,
        order_id: int,
        status: str,
    ):
        super().__init__(
            f"Order {order_id} cannot be confirmed "
            f"because its status is {status}"
        )

class PaymentAlreadyExistsError(AppException):
    status_code = HTTPStatus.CONFLICT
    error_code = "PAYMENT_ALREADY_EXISTS"

    def __init__(self, order_id: int):
        super().__init__(
            f"Order {order_id} already has a pending payment"
        )


class OrderCannotBePaidError(AppException):
    status_code = HTTPStatus.CONFLICT
    error_code = "ORDER_CANNOT_BE_PAID"

    def __init__(
        self,
        order_id: int,
        status: str,
    ):
        super().__init__(
            f"Order {order_id} cannot be paid "
            f"because its status is {status}"
        )

class PaymentNotFoundError(AppException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "PAYMENT_NOT_FOUND"

    def __init__(self, payment_id: int):
        super().__init__(
            f"Payment with id {payment_id} not found"
        )


class PaymentAlreadyFailedError(AppException):
    status_code = HTTPStatus.CONFLICT
    error_code = "PAYMENT_ALREADY_FAILED"

    def __init__(self, payment_id: int):
        super().__init__(
            f"Payment {payment_id} has already failed"
        )

class PaymentAlreadySucceededError(AppException):
    status_code = HTTPStatus.CONFLICT
    error_code = "PAYMENT_ALREADY_SUCCEEDED"

    def __init__(self, payment_id: int):
        super().__init__(
            f"Payment {payment_id} has already succeeded"
        )

class PaymentAmountMismatchError(AppException):
    status_code = HTTPStatus.CONFLICT
    error_code = "PAYMENT_AMOUNT_MISMATCH"

    def __init__(
        self,
        payment_id: int,
        expected: str,
        received: str,
    ):
        super().__init__(
            f"Payment {payment_id} amount mismatch: "
            f"expected {expected}, received {received}"
        )


class PaymentWebhookInvalidEventError(AppException):
    status_code = HTTPStatus.CONFLICT
    error_code = "PAYMENT_WEBHOOK_INVALID_EVENT"

    def __init__(
        self,
        event_type: str,
        payment_id: int,
    ):
        super().__init__(
            f"Webhook event '{event_type}' cannot be applied "
            f"to payment {payment_id}"
        )