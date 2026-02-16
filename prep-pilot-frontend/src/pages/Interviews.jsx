import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/api";

export default function Interviews() {
  const [role, setRole] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [interviews, setInterviews] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadInterviews();
  }, []);

  const loadInterviews = async () => {
    const res = await api("/interviews/"); // trailing slash IMPORTANT
    setInterviews(res);
  };

  const inProgressInterviews = interviews.filter(
    (i) => !i.is_completed
  );

  const completedInterviews = interviews.filter(
    (i) => i.is_completed
  );

  const createInterview = async () => {
    if (!role || !difficulty) {
      alert("Role and difficulty are required");
      return;
    }

    try {
      setLoading(true);
      // Create interview
      const interview = await api("/interviews/", {
        method: "POST",
        body: { role, difficulty },
      });

      //  Generate questions
      await api(`/questions/${interview.id}`, {
        method: "POST",
      });

      //  UPDATE STATE IMMEDIATELY 
      setInterviews((prev) => [...prev, interview]);

      // Reset form
      setRole("");
      setDifficulty("");

      // Navigate
      navigate(`/questions/${interview.id}`);
    } catch (err) {
      console.error(err);
      alert("Failed to create interview");
    } finally {
      setLoading(false); 
    }
  };

  return (
    <div>
    {/* CREATE INTERVIEW */}
    <h2>Create Interview</h2>

    <div className="create-interview">
      <input
        placeholder="Role (e.g. Python Developer)"
        value={role}
        onChange={(e) => setRole(e.target.value)}
      />

      <input
        placeholder="Difficulty (Easy / Medium / Hard)"
        value={difficulty}
        onChange={(e) => setDifficulty(e.target.value)}
      /><br></br><br></br>

      <button onClick={createInterview}disabled={loading}
  style={{
    padding: "10px 20px",
    backgroundColor: loading ? "#94a3b8" : "#2563eb",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: loading ? "not-allowed" : "pointer",
    fontWeight: "500",
    minWidth: "160px"
  }}
>
  {loading ? (
    <span style={{ display: "flex", alignItems: "center", gap: "8px" }}>
      <span className="spinner"></span>
      Creating...
    </span>
  ) : (
    "Create Interview"
  )}
      </button>
    </div>
      <h2>My Interviews</h2>

{/* IN PROGRESS SECTION */}
<h3 style={{ marginTop: "20px" }}>In Progress</h3>

{inProgressInterviews.length === 0 ? (
  <p style={{ color: "#777" }}>No interviews in progress</p>
) : (
  <div className="interview-grid">
    {inProgressInterviews.map((i) => (
      <div
        key={i.id}
        className="interview-card"
        onClick={() => navigate(`/questions/${i.id}`)}
      >
        <div className="role-row">
  <h3 className="role-title">{i.role}</h3>

  <span className={`difficulty-badge ${i.difficulty.toLowerCase()}`}>
    {i.difficulty}
  </span>
</div>

        <p className="created-at">
          Created on:{" "}
          {i.created_at
            ? new Date(i.created_at).toLocaleString()
            : "—"}
        </p>

        <div className="status in-progress">
          In Progress ⏳
        </div>
      </div>
    ))}
  </div>
)}

{/* COMPLETED SECTION */}
<h3 style={{ marginTop: "30px" }}>Completed</h3>

{completedInterviews.length === 0 ? (
  <p style={{ color: "#777" }}>No completed interviews</p>
) : (
  <div className="interview-grid">
    {completedInterviews.map((i) => (
      <div
        key={i.id}
        className="interview-card"
        onClick={() => navigate(`/questions/${i.id}`)}
      >
        <div className="role-row">
  <h3 className="role-title">{i.role}</h3>

  <span className={`difficulty-badge ${i.difficulty.toLowerCase()}`}>
    {i.difficulty}
  </span>
</div>

        <p className="created-at">
          Created on:{" "}
          {i.created_at
            ? new Date(i.created_at).toLocaleString()
            : "—"}
        </p>

        <div className="status completed">
          Completed ✅
        </div>
      </div>
    ))}
  </div>
)}
    </div>
  );
}
