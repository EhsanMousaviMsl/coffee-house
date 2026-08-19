import ProductCard from "./ProductCard";

export default function ProductList({
  products,
  onAddToCart,
}) {
  return (
    <section className="products-section">
      <h2>Our Menu</h2>

      <div className="products-grid">
        {products.map((product) => (
          <ProductCard
            key={product.id}
            product={product}
            onAddToCart={onAddToCart}
          />
        ))}
      </div>
    </section>
  );
}