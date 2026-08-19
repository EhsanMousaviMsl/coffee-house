const API_URL = import.meta.env.VITE_API_URL;

export async function succeedPayment(paymentId) {
  const response = await fetch(
    `${API_URL}/payments/${paymentId}/simulate-success`,
    {
      method: "POST",
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Payment failed");
  }

  return response.json();
}


export async function failPayment(paymentId) {
  const response = await fetch(
    `${API_URL}/payments/${paymentId}/simulate-failure`,
    {
      method: "POST",
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Payment failed");
  }

  return response.json();
}