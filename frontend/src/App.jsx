import React, { useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useNavigate,
} from "react-router-dom";

import Home from "./components/Home";
import Login from "./components/Login";
import Register from "./components/Register";
import Cart from "./components/Cart";
import AdminPanel from "./components/AdminPanel";
import "./App.css";

function NavBar({ user, setUser }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    setUser(null);
    navigate("/");
  };

  return (
    <nav id="top_margin">
      <Link to="/" style={{ marginRight: 15 }}>
        <button id="home">🏠Home</button>
      </Link>
      <Link to="/cart" style={{ marginRight: 15 }}>
        <button id="home">🛒My Cart</button>
      </Link>

      {user ? (
        <>
          <span style={{ marginRight: 15 }}>Welcome, {user.name}!</span>

          {user.role === "admin" && (
            <Link to="/admin" style={{ marginRight: 15 }}>
              <button id="home">🛠 Admin</button>
            </Link>
          )}

          <button onClick={handleLogout} id="home">
            Logout
          </button>
        </>
      ) : (
        <>
          <Link to="/login" style={{ marginRight: 15 }}>
            <button id="home">🔑Login</button>
          </Link>
          <Link to="/register">
            <button id="home">📝Register</button>
          </Link>
        </>
      )}
    </nav>
  );
}

function App() {
  const [user, setUser] = useState(null);

  return (
    <Router>
      <NavBar user={user} setUser={setUser} />

      <Routes>
        <Route path="/" element={<Home user={user} />} />
        <Route path="/login" element={<Login setUser={setUser} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/cart" element={<Cart user={user} />} />
        <Route
          path="/admin"
          element={
            user?.role === "admin" ? (
              <AdminPanel user={user} />
            ) : (
              <div style={{ padding: 20, textAlign: "center" }}>
                🚫 Access Denied: Admins Only
              </div>
            )
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
