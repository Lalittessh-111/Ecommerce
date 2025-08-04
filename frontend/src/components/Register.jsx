import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Register.css";

function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    role: "user", // default role
  });

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:8888/register", formData);
      alert(res.data.message);
      navigate("/login");
    } catch (err) {
      alert(err.response?.data?.message || "Registration failed");
    }
  };

  return (
    <div id="reg_back">
      <h2 style={{ textAlign: "center", paddingTop: "20px" }}>Register</h2>
      <form onSubmit={handleSubmit} style={{ width: "300px", margin: "auto" }}>
        <div style={{ marginBottom: "15px" }}>
          <label>Name:</label>
          <br />
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            style={{ width: "100%", padding: "8px" }}
          />
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label>Email:</label>
          <br />
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            style={{ width: "100%", padding: "8px" }}
          />
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label>Password:</label>
          <br />
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            style={{ width: "100%", padding: "8px" }}
          />
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label>Role:</label>
          <br />
          <select
            name="role"
            value={formData.role}
            onChange={handleChange}
            style={{ width: "100%", padding: "8px" }}
          >
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <button id="reg_button" type="submit">
          Register
        </button>

        <p style={{ textAlign: "center", marginTop: "20px" }}>
          Already have an account?{" "}
          <button
            style={{
              background: "none",
              color: "#4a90e2",
              border: "none",
              cursor: "pointer",
              fontWeight: "bold",
              textDecoration: "underline",
            }}
            onClick={() => navigate("/login")}
          >
            Login Here
          </button>
        </p>
      </form>
    </div>
  );
}

export default Register;
