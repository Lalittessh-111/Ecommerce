import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import "./Login.css";

function Login({ setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    axios
      .post("http://localhost:8888/login", { email, password })
      .then((res) => {
        if (res.data.status === "success") {
          const userData = {
            user_id: res.data.user_id,
            name: res.data.name,
            role: res.data.role,
          };

          setUser(userData);

          //  Redirect admin to /admin, others to /
          if (userData.role === "admin") {
            navigate("/admin");
          } else {
            navigate("/");
          }
        } else {
          setError(res.data.message || "Login failed");
        }
      })
      .catch((err) => {
        setError("Incorrect email or password");
        console.error(err);
      });
  };

  return (
    <div id="log_back">
      <h2>Login</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleLogin}>
        <div>
          <label>Email:</label>
          <br />
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Password:</label>
          <br />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <p></p>
        <button type="submit" id="login">
          Login
        </button>
      </form>

      <p>
        Don't have an account? <Link to="/register">Register here</Link>
      </p>
    </div>
  );
}

export default Login;
