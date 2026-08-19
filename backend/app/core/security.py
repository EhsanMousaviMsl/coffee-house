import hashlib
import hmac


def generate_webhook_signature(
    payload: bytes,
    secret: str,
) -> str:
    return hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()


def verify_webhook_signature(
    payload: bytes,
    signature: str,
    secret: str,
) -> bool:
    expected_signature = generate_webhook_signature(
        payload,
        secret,
    )

    return hmac.compare_digest(
        expected_signature,
        signature,
    )