import { Outlet, Link, useNavigate } from "react-router-dom";

export default function Layout() {
  const navigate = useNavigate();
  const role = localStorage.getItem("role");

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  // Professional link style
  const linkStyle = {
    textDecoration: "none",
    color: "#ffffff",
    padding: "10px 12px",
    borderRadius: "8px",
    fontSize: "17px",
    fontWeight: "550",
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>

      {/* ✅ PROFESSIONAL SIDEBAR */}
      <div
        style={{
          width: "280px",
          backgroundColor: "#0a1d49f0",
          color: "white",
          padding: "30px 20px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
        }}
      >
        {/* Top Section */}
        <div>
          {/* Logo */}
          <h2
            style={{
              fontSize: "28px",
              fontWeight: "650",
              letterSpacing: "0.5px",
              marginBottom: "40px",
            }}
          >
            PrepPilot AI
          </h2>

          {/* Navigation Links */}
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            <Link to="/dashboard" style={linkStyle}>Dashboard</Link>
            <Link to="/dashboard/profile" style={linkStyle}>Profile</Link>
            <Link to="/dashboard/settings" style={linkStyle}>Settings</Link>
          </div>
        </div>

        {/* Bottom Logout Button */}
        <button
          onClick={handleLogout}
          style={{
            padding: "10px",
            backgroundColor: "#445a7e",
            color: "white",
            border: "2px solid #9ea1a6",
            borderRadius: "8px",
            cursor: "pointer",
            fontWeight: "600",
          }}
        >
          Logout
        </button>
      </div>

      {/* Main Content */}
      <div
        style={{
          flex: 1,
          padding: "40px",
          backgroundColor: "#daebfda5",
        }}
      >
        <Outlet />
      </div>

    </div>
  );
}
