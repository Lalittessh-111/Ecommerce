import React, { useState } from "react";
import "./OrderForm.css";

function OrderForm({ product, user, onClose }) {
  const [mobile, setMobile] = useState("");
  const [address, setAddress] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <div className="order-modal">
        <div className="order-content">
          <p>Dear {user.name}, your order has been completed.</p>
          <p>Your product will be delivered to:</p>
          <p><strong>{address}</strong></p>
          <button onClick={onClose}id="order">Close</button>
        </div>
      </div>
    );
  }

  return (
    <div className="order-modal">
      <div className="order-content">
        <h3>Place Order</h3>
        <form onSubmit={handleSubmit}>
          <label>Name:</label>
          <input type="text" value={user.name} disabled />

          <label>Product:</label>
          <input type="text" value={product.name} disabled />

          <label>Mobile Number:</label>
          <input type="text" value={mobile} onChange={e => setMobile(e.target.value)} required />

          <label>Address:</label>
          <textarea value={address} onChange={e => setAddress(e.target.value)} required />
            <p></p>

          <button type="submit" id="order">Place Order</button>
          <button type="button" onClick={onClose} className="cancel-btn">Cancel</button>
        </form>
      </div>
    </div>
  );
}

export default OrderForm;
