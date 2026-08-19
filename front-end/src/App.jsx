import { useEffect, useState } from "react";

import { getProducts } from "./api/products";

import {
  createOrder,
  getOrder,
  cancelOrder,
} from "./api/orders";

import { createPayment } from "./api/payments";

import {
  succeedPayment,
  failPayment,
} from "./api/paymentSimulation";

import Cart from "./components/Cart";
import OrderConfirmation from "./components/OrderConfirmation";
import ProductList from "./components/ProductList";


function App() {
  const [products, setProducts] = useState([]);

  const [cart, setCart] = useState([]);

  const [order, setOrder] = useState(null);
  const [checkoutLoading, setCheckoutLoading] = useState(false);

  const [payment, setPayment] = useState(null);
  const [paymentLoading, setPaymentLoading] = useState(false);

  const [screen, setScreen] = useState("menu");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


  // -------------------------
  // Load products
  // -------------------------

  useEffect(() => {
    async function loadProducts() {
      try {
        const data = await getProducts();

        setProducts(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadProducts();
  }, []);


  // -------------------------
  // Cart
  // -------------------------

  function addToCart(product) {
    setCart((currentCart) => {
      const existingItem = currentCart.find(
        (item) => item.id === product.id
      );

      if (existingItem) {
        return currentCart.map((item) =>
          item.id === product.id
            ? {
                ...item,
                quantity: item.quantity + 1,
              }
            : item
        );
      }

      return [
        ...currentCart,
        {
          ...product,
          quantity: 1,
        },
      ];
    });
  }


  function increaseQuantity(productId) {
    setCart((currentCart) =>
      currentCart.map((item) =>
        item.id === productId
          ? {
              ...item,
              quantity: item.quantity + 1,
            }
          : item
      )
    );
  }


  function decreaseQuantity(productId) {
    setCart((currentCart) =>
      currentCart
        .map((item) =>
          item.id === productId
            ? {
                ...item,
                quantity: item.quantity - 1,
              }
            : item
        )
        .filter((item) => item.quantity > 0)
    );
  }


  function removeFromCart(productId) {
    setCart((currentCart) =>
      currentCart.filter(
        (item) => item.id !== productId
      )
    );
  }


  // -------------------------
  // Order
  // -------------------------

  async function checkout() {
    if (cart.length === 0) {
      return;
    }

    try {
      setCheckoutLoading(true);

      const createdOrder = await createOrder(cart);

      setOrder(createdOrder);
    } catch (error) {
      alert(error.message);
    } finally {
      setCheckoutLoading(false);
    }
  }


  async function cancelCurrentOrder() {
    if (!order) {
      return;
    }

    const confirmed = window.confirm(
      `Are you sure you want to cancel Order #${order.id}?`
    );

    if (!confirmed) {
      return;
    }

    try {
      setCheckoutLoading(true);

      await cancelOrder(order.id);

      setOrder(null);
      setPayment(null);

      setScreen("menu");
    } catch (error) {
      alert(error.message);
    } finally {
      setCheckoutLoading(false);
    }
  }


  // -------------------------
  // Payment
  // -------------------------

  async function continueToPayment() {
    if (!order) {
      return;
    }

    try {
      setPaymentLoading(true);

      const createdPayment = await createPayment(
        order.id
      );

      setPayment(createdPayment);
    } catch (error) {
      alert(error.message);
    } finally {
      setPaymentLoading(false);
    }
  }


  async function pay() {
    if (!payment) {
      return;
    }

    try {
      setPaymentLoading(true);

      const updatedPayment =
        await succeedPayment(payment.id);

      setPayment(updatedPayment);

      // Get the updated order because
      // the webhook changes order status
      const updatedOrder =
        await getOrder(order.id);

      setOrder(updatedOrder);

      setScreen("confirmation");
    } catch (error) {
      alert(error.message);
    } finally {
      setPaymentLoading(false);
    }
  }


  async function failPaymentAttempt() {
    if (!payment) {
      return;
    }

    try {
      setPaymentLoading(true);

      const updatedPayment =
        await failPayment(payment.id);

      setPayment(updatedPayment);
    } catch (error) {
      alert(error.message);
    } finally {
      setPaymentLoading(false);
    }
  }


  async function retryPayment() {
    if (!order) {
      return;
    }

    try {
      setPaymentLoading(true);

      const newPayment =
        await createPayment(order.id);

      setPayment(newPayment);
    } catch (error) {
      alert(error.message);
    } finally {
      setPaymentLoading(false);
    }
  }


  // -------------------------
  // Loading
  // -------------------------

  if (loading) {
    return <p>Loading products...</p>;
  }


  // -------------------------
  // Error
  // -------------------------

  if (error) {
    return <p>Error: {error}</p>;
  }


  // -------------------------
  // Confirmation screen
  // -------------------------

  if (screen === "confirmation") {
    return (
      <OrderConfirmation
        order={order}
        payment={payment}
        onBackToMenu={() => {
          setCart([]);
          setOrder(null);
          setPayment(null);
          setScreen("menu");
        }}
      />
    );
  }


  // -------------------------
  // Main application
  // -------------------------

  return (
    <div className="app">

      {/* Header */}

      <header className="header">
        <div className="header-content">

          <h1>☕ Coffee House</h1>

          <div className="cart-indicator">
            🛒{" "}
            {cart.reduce(
              (total, item) =>
                total + item.quantity,
              0
            )}
          </div>

        </div>
      </header>


      <main className="main-content">

        {/* Products */}

        <ProductList
          products={products}
          onAddToCart={addToCart}
        />


        {/* Cart */}

        <Cart
          items={cart}
          onIncrease={increaseQuantity}
          onDecrease={decreaseQuantity}
          onRemove={removeFromCart}
          onCheckout={checkout}
          checkoutLoading={checkoutLoading}
        />


        {/* Order */}

        {order &&
          order.status === "pending" && (
            <section className="order-section">

              <h2>
                Order #{order.id}
              </h2>

              <p>
                <strong>Status:</strong>{" "}
                {order.status}
              </p>

              <p>
                <strong>Total:</strong>{" "}
                €{order.total_price}
              </p>


              <div className="order-actions">

                <button
                  onClick={continueToPayment}
                  disabled={paymentLoading}
                >
                  {paymentLoading
                    ? "Creating payment..."
                    : "Continue to payment"}
                </button>


                <button
                  className="secondary-button"
                  onClick={cancelCurrentOrder}
                  disabled={
                    checkoutLoading ||
                    paymentLoading
                  }
                >
                  Change order
                </button>

              </div>

            </section>
          )}


        {/* Payment */}

        {payment && (
          <section className="payment-section">

            <h2>Payment</h2>

            <p>
              <strong>Payment:</strong>{" "}
              #{payment.id}
            </p>

            <p>
              <strong>Amount:</strong>{" "}
              €{payment.amount}
            </p>

            <p>
              <strong>Status:</strong>{" "}
              {payment.status}
            </p>


            {/* Pending payment */}

            {payment.status === "pending" && (
              <div className="payment-demo">

                <h3>💳 Payment Demo</h3>

                <button
                  onClick={pay}
                  disabled={paymentLoading}
                >
                  {paymentLoading
                    ? "Processing..."
                    : `Pay €${payment.amount}`}
                </button>


                <button
                  className="secondary-button"
                  onClick={failPaymentAttempt}
                  disabled={paymentLoading}
                >
                  Simulate failure
                </button>

              </div>
            )}


            {/* Successful payment */}

            {payment.status === "succeeded" && (
              <div className="payment-success">

                <h3>
                  ✅ Payment successful!
                </h3>

                <p>
                  Your order has been paid.
                </p>

              </div>
            )}


            {/* Failed payment */}

            {payment.status === "failed" && (
              <div className="payment-failed">

                <h3>
                  ❌ Payment failed
                </h3>

                <p>
                  Your payment could not
                  be completed.
                </p>


                <button
                  onClick={retryPayment}
                  disabled={paymentLoading}
                >
                  {paymentLoading
                    ? "Creating payment..."
                    : "Try again"}
                </button>

              </div>
            )}

          </section>
        )}

      </main>

    </div>
  );
}


export default App;