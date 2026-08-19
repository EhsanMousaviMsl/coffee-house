const API_URL = import.meta.env.VITE_API_URL 

export async function createPayment(orderId) {
  const response = await fetch(`${API_URL}/payments/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      order_id: orderId,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Failed to create payment");
  }

  return response.json();
}