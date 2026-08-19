function Cart({ items, onIncrease, onDecrease, onRemove, onCheckout, checkoutLoading }) {
  const total = items.reduce(
    (sum, item) => sum + Number(item.price) * item.quantity,
    0
  );

  if (items.length === 0) {
    return (
      <div>
        <h2>Your Cart</h2>
        <p>Your cart is empty.</p>
      </div>
    );
  }

  return (
    <div>
      <h2>Your Cart</h2>

      {items.map((item) => (
        <div key={item.id}>
          <h3>{item.name}</h3>

          <p>
            €{item.price} × {item.quantity}
          </p>

          <button onClick={() => onDecrease(item.id)}>
            -
          </button>

          <span> {item.quantity} </span>

          <button onClick={() => onIncrease(item.id)}>
            +
          </button>

          <button onClick={() => onRemove(item.id)}>
            Remove
          </button>
        </div>
      ))}

      <h3>Total: €{total.toFixed(2)}</h3>

      <button
        onClick={onCheckout}
        disabled={checkoutLoading}
        >
        {checkoutLoading ? "Creating order..." : "Checkout"}
      </button>
    </div>
  );
}

export default Cart;