import React, { useEffect, useState } from "react";
import axios from "axios";
import OrderForm from "./OrderForm";

function Cart({ user }) {
  const [cartItems, setCartItems] = useState([]);
  const [message, setMessage] = useState("");
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [showOrderForm, setShowOrderForm] = useState(false);

  useEffect(() => {
    if (user) {
      axios
        .get(`http://localhost:8888/cart/${user.user_id}`)
        .then((res) => {
          if (res.data.status === "success") {
            setCartItems(res.data.cart);
            setMessage("");
          } else {
            setMessage(res.data.message);
          }
        })
        .catch((err) => {
          setMessage("Failed to fetch cart items.");
          console.error(err);
        });
    } else {
      const guestCart = JSON.parse(localStorage.getItem("guestCart") || "[]");
      if (guestCart.length === 0) {
        setCartItems([]);
        return;
      }

      axios
        .get("http://localhost:8888/products")
        .then((res) => {
          if (res.data.status === "success") {
            const filtered = res.data.products.filter((p) =>
              guestCart.includes(p.productid)
            );
            setCartItems(filtered);
            setMessage("");
          }
        })
        .catch((err) => {
          console.error(err);
          setMessage("Failed to load guest cart.");
        });
    }
  }, [user]);

  const handleRemove = (product_id) => {
    if (user) {
      axios
        .delete("http://localhost:8888/cart", {
          data: { user_id: user.user_id, product_id },
        })
        .then((res) => {
          if (res.data.status === "success") {
            setCartItems((prev) =>
              prev.filter((item) => item.productid !== product_id)
            );
          } else {
            setMessage(res.data.message);
          }
        })
        .catch((err) => {
          setMessage("Failed to remove product.");
          console.error(err);
        });
    } else {
      let guestCart = JSON.parse(localStorage.getItem("guestCart") || "[]");
      guestCart = guestCart.filter((id) => id !== product_id);
      localStorage.setItem("guestCart", JSON.stringify(guestCart));
      setCartItems((prev) =>
        prev.filter((item) => item.productid !== product_id)
      );
    }
  };

  const handleOrderClick = (product) => {
    if (!user) {
      alert("Please login to place an order.");
      return;
    }
    setSelectedProduct(product);
    setShowOrderForm(true);
  };

  return (
    <div>
      <h2>My Cart</h2>
      {message && <p style={{ color: "green" }}>{message}</p>}

      {cartItems.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}>
          {cartItems.map((item) => (
            <div
              key={item.productid}
              style={{ border: "1px solid #ccc", padding: 10, width: 250 }}
            >
              <img
                src={item.image}
                alt={item.name}
                style={{ width: "100%", height: 150, objectFit: "cover" }}
              />
              <h4>{item.name}</h4>
              <p>Category: {item.category}</p>
              <p>Price: ₹{(item.price * 80).toFixed(2)}</p>
              <button
                onClick={() => handleRemove(item.productid)}
                style={{ backgroundColor: "#406f70" }}
              >
                Remove
              </button>{" "}
              <button
                onClick={() => handleOrderClick(item)}
                style={{ marginLeft: "80px", backgroundColor: "#fc4e03" }}
              >
                Place Order
              </button>
            </div>
          ))}
        </div>
      )}

      {showOrderForm && selectedProduct && (
        <OrderForm
          product={selectedProduct}
          user={user}
          onClose={() => setShowOrderForm(false)}
        />
      )}
    </div>
  );
}

export default Cart;
