import json
from decimal import Decimal

from app.core.security import generate_webhook_signature
from app.models.order import Order, OrderStatus
from app.models.payment import Payment, PaymentStatus
from app.models.payment_webhook_event import PaymentWebhookEvent
from app.core.config import settings


def test_payment_succeeded_webhook(
    client,
    db,
):
    # Arrange
    order = Order(
        status=OrderStatus.PENDING,
        total_price=Decimal("10.00"),
    )

    db.add(order)
    db.flush()

    payment = Payment(
        order_id=order.id,
        amount=Decimal("10.00"),
        status=PaymentStatus.PENDING,
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    payload = {
        "event_id": "evt_test_001",
        "event_type": "payment.succeeded",
        "payment_id": payment.id,
        "amount": "10.00",
    }

    raw_body = json.dumps(payload).encode()

    signature = generate_webhook_signature(
        payload=raw_body,
        secret= settings.payment_webhook_secret,
    )
    # Act
    response = client.post(
        "/api/v1/webhooks/payment",
        content=raw_body,
        headers={
            "Content-Type": "application/json",
            "X-Webhook-Signature": signature,
        },
    )

    duplicate_response = client.post(
        "/api/v1/webhooks/payment",
        content=raw_body,
        headers={
            "Content-Type": "application/json",
            "X-Webhook-Signature": signature,
        },
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "received": True,
    }

    assert duplicate_response.status_code == 200
    assert duplicate_response.json() == {
        "received": True,
    }

    
    db.expire_all()

    payment = db.get(Payment, payment.id)
    order = db.get(Order, order.id)

    assert payment.status == PaymentStatus.SUCCEEDED
    assert order.status == OrderStatus.CONFIRMED

    webhook_event = db.query(
        PaymentWebhookEvent
    ).filter(
        PaymentWebhookEvent.event_id == "evt_test_001"
    ).one()

    assert webhook_event.payment_id == payment.id
    
    webhook_event_count = db.query(
    PaymentWebhookEvent
).filter(
    PaymentWebhookEvent.event_id == "evt_test_001"
).count()

    assert webhook_event_count == 1