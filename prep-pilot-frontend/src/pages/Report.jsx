import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import { api } from "../api/api";

export default function Report() {
  const { interviewId } = useParams();
  const navigate = useNavigate();

  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);


  useEffect(() => {
    loadReport();
  }, [interviewId]);

  const loadReport = async () => {
    try {
      const res = await api(`/reports/${interviewId}`);
      setReport(res);
    } catch (err) {
      console.error(err);

      if (err.message?.includes("Interview not completed")) {
        alert("Please answer all questions to view the report.");
        navigate(`/questions/${interviewId}`);
      } else {
        alert("Failed to load interview report");
      }
    }   finally {
      setLoading(false);
    }
  };

  if (loading) return <p>Loading interview report...</p>;
  if (!report) return <p>No report available.</p>;

  const downloadPDF = async () => {
  try {
    setDownloading(true);
    const token = localStorage.getItem("token");

    const response = await fetch(
      `https://preppilot-backend.onrender.com/reports/interview/${interviewId}/pdf`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error("Failed to download PDF");
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = `Interview_Report_${interviewId}.pdf`;
    document.body.appendChild(a);
    a.click();

    a.remove();
    window.URL.revokeObjectURL(url);
    alert("PDF downloaded successfully ✅");
  } catch (err) {
    console.error(err);
    alert("Could not download PDF report");
  } finally {
    setDownloading(false);
  }
};


  return (
  <div className="report-container">
    <div className="report-header">
  <h2 className="report-title">Interview Report</h2>

  <button className="download-btn" onClick={downloadPDF} disabled={downloading}>
    {downloading ? "⏳ Generating PDF..." : "📄 Download PDF"}
  </button>
</div>

    {/* Interview */}
    <div className="report-meta">
      <div>
        <span className="label">Role</span>
        <p>{report.role}</p>
      </div>
      <div>
        <span className="label">Difficulty</span>
        <p>{report.difficulty}</p>
      </div>
      <div>
        <span className="label">Average Score</span>
        <p className="avg-score">
          {report.avg_score !== null
            ? `${report.avg_score.toFixed(1)} / 10`
            : "N/A"}
        </p>
      </div>
    </div>

    {/* Questions */}
    <h3 className="section-title">Question-wise Evaluation</h3>

    <div className="report-questions">
      {report.questions.map((q, index) => (
        <div key={q.id} className="report-question-card">
          <h4>Q{index + 1}. {q.question_text}</h4>

          <div className="answer-block">
            <span>Your Answer</span>
            <p>{q.user_answer ?? "Not answered"}</p>
          </div>

          <div className="feedback-row">
            <div>
              <span>Score</span>
              <p className={`score ${q.score >= 6 ? "good" : "bad"}`}>
                {q.score !== null ? `${q.score}/10` : "N/A"}
              </p>
            </div>

            <div>
              <span>Feedback</span>
              <p>{q.feedback ?? "No feedback"}</p>
            </div>
          </div>
        </div>
      ))}
    </div>

    {/* Overall Verdict */}
    <h3>Overall AI Verdict</h3>
    <div className="verdict-box">
      <ReactMarkdown>
        {report.overall_verdict ?? "No overall evaluation available"}
      </ReactMarkdown>
    </div>

    <button
      className="back-btn"
      onClick={() => navigate("/interviews")}
    >
      ← Back to My Interviews
    </button>
  </div>
);

}
