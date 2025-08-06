import React, { useEffect, useState } from "react";
import axios from "axios";
import "./AdminPanel.css";

function AdminPanel({ user }) {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({
    name: "",
    category: "",
    price: "",
    image: "",
    product_id: null,
  });
  const [isEdit, setIsEdit] = useState(false);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await axios.get("http://localhost:8888/products");
        setProducts(res.data.products);
      } catch (err) {
        alert("Failed to load products");
        console.error("Product Fetch Error:", err);
      }
    };

    fetchProducts();
  }, []);

  if (!user || !user.user_id) {
    return <div> Admin user not loaded. Please login again.</div>;
  }

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const url = isEdit
      ? "http://localhost:8888/admin/product/edit"
      : "http://localhost:8888/admin/product/add";

    try {
      const payload = {
        user_id: user.user_id,
        name: form.name,
        category: form.category,
        price: parseFloat(form.price),
        image: form.image,
        ...(isEdit && { product_id: form.product_id }),
      };

      await axios({
        method: isEdit ? "put" : "post",
        url,
        headers: { "Content-Type": "application/json" },
        data: payload,
      });

      alert(isEdit ? "Product updated!" : "Product added!");
      const res = await axios.get("http://localhost:8888/products");
      setProducts(res.data.products);
      setForm({
        name: "",
        category: "",
        price: "",
        image: "",
        product_id: null,
      });
      setIsEdit(false);
    } catch (err) {
      alert(err.response?.data?.message || "Failed to submit");
      console.error("Submit Error:", err.response || err);
    }
  };

  const handleEdit = (product) => {
    setForm({
      name: product.name,
      category: product.category,
      price: product.price,
      image: product.image,
      product_id: product.productid,
    });
    setIsEdit(true);
  };

  const handleDelete = async (productId) => {
    try {
      await axios.delete("http://localhost:8888/admin/product/delete", {
        headers: { "Content-Type": "application/json" },
        data: { product_id: productId, user_id: user.user_id },
      });
      alert("Product deleted!");
      const res = await axios.get("http://localhost:8888/products");
      setProducts(res.data.products);
    } catch (err) {
      alert(err.response?.data?.message || "Failed to delete");
      console.error("Delete Error:", err.response || err);
    }
  };

  return (
    <div className="admin-container">
      <h2>Admin Product Control Panel</h2>
      <form onSubmit={handleSubmit} className="admin-form">
        <input
          name="name"
          placeholder="Name"
          value={form.name}
          onChange={handleChange}
          required
        />
        <input
          name="category"
          placeholder="Category"
          value={form.category}
          onChange={handleChange}
          required
        />
        <input
          name="price"
          type="number"
          placeholder="Price"
          value={form.price}
          onChange={handleChange}
          required
        />
        <input
          name="image"
          placeholder="Image URL"
          value={form.image}
          onChange={handleChange}
          required
        />
        <button type="submit">{isEdit ? "Update" : "Add"} Product</button>
      </form>

      <table className="admin-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Category</th>
            <th>Price</th>
            <th>Image</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {products.map((prod) => (
            <tr key={prod.productid}>
              <td>{prod.name}</td>
              <td>{prod.category}</td>
              <td>₹{prod.price}</td>
              <td>
                <img src={prod.image} alt={prod.name} width="50" />
              </td>
              <td>
                <button onClick={() => handleEdit(prod)}>Edit</button>
                <button onClick={() => handleDelete(prod.productid)}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminPanel;
