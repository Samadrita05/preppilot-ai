import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../api/api";

export default function Questions() {
  const { interviewId } = useParams();
  const navigate = useNavigate();

  const [questions, setQuestions] = useState([]);
  const [answeredQuestionIds, setAnsweredQuestionIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isCompleted, setIsCompleted] = useState(false);

  useEffect(() => {
    loadQuestions();
  }, [interviewId]);

  const loadQuestions = async () => {
    try {
      const res = await api(`/questions/${interviewId}`);
      setQuestions(res.questions || []);

      const answers = await api(`/answers/interview/${interviewId}`);
      setAnsweredQuestionIds(answers.map(a => a.question_id));

      const interview = await api(`/interviews/${interviewId}`);
      setIsCompleted(interview.is_completed);
    } catch (err) {
      console.error(err);
      setQuestions([]);
    } finally {
      setLoading(false);
    }
  };

  const generateQuestions = async () => {
    try {
      await api(`/questions/${interviewId}`, { method: "POST" });
      await loadQuestions();
    } catch (err) {
      console.error(err);
      alert("Failed to generate questions");
    }
  };

  if (loading) return <p>Loading questions...</p>;

  return (
  <div className="container">
    <h2>Questions</h2>

    {isCompleted && (
      <p className="completed-banner">
        Interview completed 🎉
      </p>
    )}

    {questions.length > 0 && (
      <p className="progress-text">
        {answeredQuestionIds.length} / {questions.length} answered
      </p>
    )}

    {questions.length > 0 && (
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{
            width: `${(answeredQuestionIds.length / questions.length) * 100}%`,
          }}
        />
      </div>
    )}

    {questions.length === 0 && !isCompleted && (
      <div className="empty-state">
        <p>No questions found. Please generate questions first.</p>
        <button onClick={generateQuestions}>
          Generate Questions
        </button>
      </div>
    )}

    <div className="question-list">
      {questions.map((q) => {
        const isAnswered = answeredQuestionIds.includes(q.id);

        return (
          <div key={q.id} className="question-card">
            <p className="question-text">{q.question_text}</p>

            <button
              disabled={isAnswered || isCompleted}
              className={isAnswered ? "btn-disabled" : "btn-primary"}
              onClick={() => navigate(`/answer/${q.id}`)}
            >
              {isAnswered ? "Answered" : "Answer"}
            </button>
          </div>
        );
      })}
    </div>

    {isCompleted && (
      <button
        className="view-report-btn"
        onClick={() => navigate(`/report/${interviewId}`)}
      >
        View Interview Report
      </button>
    )}
  </div>
);

}
