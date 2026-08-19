const API_URL = import.meta.env.VITE_API_URL 

export async function createOrder(items) {
  const response = await fetch(`${API_URL}/orders/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      items: items.map((item) => ({
        product_id: item.id,
        quantity: item.quantity,
      })),
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Failed to create order");
  }

  return response.json();
}

export async function getOrder(orderId) {
  const response = await fetch(`${API_URL}/orders/${orderId}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Failed to fetch order");
  }

  return response.json();
}


export async function cancelOrder(orderId) {
  const response = await fetch(
    `${API_URL}/orders/${orderId}/cancel`,
    {
      method: "POST",
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Failed to cancel order");
  }

  return response.json();
}

