export default function ProductCard({ product, onAddToCart }) {
  return (
    <article className="product-card">
      <h3>{product.name}</h3>

      <p>{product.description}</p>

      <p className="product-price">
        €{product.price}
      </p>

      <button onClick={() => onAddToCart(product)}>
        Add to cart
      </button>
    </article>
  );
}