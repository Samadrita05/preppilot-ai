import { useState } from "react";

export default function Profile() {
  const email = localStorage.getItem("email");
  const [name, setName] = useState(localStorage.getItem("name") || "");

  const handleSave = () => {
    localStorage.setItem("name", name);
    alert("Profile updated successfully!");
  };

  return (
    <div
      style={{
        maxWidth: "600px",
        background: "white",
        padding: "40px",
        borderRadius: "10px",
        boxShadow: "0 4px 10px rgba(0, 0, 0, 0.17)",
      }}
    >
      <h2 style={{ marginBottom: "25px" }}> 👤 Profile</h2>

      {/* Name */}
      <div style={{ marginBottom: "15px" }}>
        <label>Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={inputStyle}
        />
      </div>

      {/* Email */}
      <div style={{ marginBottom: "30px" }}>
        <label>Email</label>
        <input
          type="text"
          value={email}
          disabled
          style={{ ...inputStyle, backgroundColor: "#f3f4f6" }}
        />
      </div>

      <button
        onClick={handleSave}
        style={{
          padding: "8px 16px",
          backgroundColor: "#2563eb",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Save Changes
      </button>
    </div>
  );
}

const inputStyle = {
  width: "100%",
  padding: "8px",
  marginTop: "5px",
  borderRadius: "5px",
  border: "1px solid #2f59a1a1",
};
