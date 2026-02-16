import { Link } from "react-router-dom";

export default function Dashboard() {
  const email = localStorage.getItem("email");

  return (
    <div style={{ maxWidth: "600px" }}>
      {/* Header */}
      <div style={{ marginBottom: "40px" }}>
        <h1 style={{ fontSize: "28.5px", fontWeight: "750" }}>
          Welcome back to PrepPilot AI 🤖
        </h1>
        <p style={{
           fontSize: "18.5px",
           color: "#494d54",
           marginTop: "8px",
           marginBottom: "6px"
          }}>
        Your personal AI-powered interview preparation assistant. </p>

        <p style={{ color: "#686c75", fontSize: "16px" }}>
         Logged in as {email}
       </p>
      </div>

      {/* Main Card */}
      <div
        style={{
          background: "white",
          padding: "30px",
          borderRadius: "12px",
          boxShadow: "0 4px 12px rgba(0, 0, 0, 0.21)",
        }}
      >
        <h3 style={{ marginBottom: "18px" }}>
          🚀 Ready for your next interview?
        </h3>

        <Link to="/interviews">
          <button
            style={{
              padding: "12px 20px",
              backgroundColor: "#2563eb",
              color: "white",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              fontWeight: "500",
              fontSize: "14px"
            }}
          >
            Go to My Interviews
          </button>
        </Link>
      </div>
    </div>
  );
}
