const API_URL = "http://127.0.0.1:8000/api/v1";

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