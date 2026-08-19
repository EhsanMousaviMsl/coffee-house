export default function OrderConfirmation({
  order,
  payment,
  onBackToMenu,
}) {
  return (
    <section>
      <h1>✅ Order confirmed!</h1>

      <p>Thank you for your order.</p>

      <div>
        <h2>Order #{order.id}</h2>

        <p>
          <strong>Total:</strong>{" "}
          €{order.total_price}
        </p>

        <p>
          <strong>Payment:</strong>{" "}
          {payment.status === "succeeded"
            ? "Paid"
            : payment.status}
        </p>

        <p>
          <strong>Status:</strong>{" "}
          {order.status}
        </p>
      </div>

      <button onClick={onBackToMenu}>
        Back to Menu
      </button>
    </section>
  );
}