import { useEffect, useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../api/api";

export default function Answer() {
  const QUESTION_TIME = 180; // 2 minutes
  const { questionId } = useParams();
  const navigate = useNavigate();
  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const [listening, setListening] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [timeLeft, setTimeLeft] = useState(QUESTION_TIME);
  const [timeUp, setTimeUp] = useState(false);
  const recognitionRef = useRef(null);


  useEffect(() => {
    loadQuestion();
  }, [questionId]);

  useEffect(() => {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) return;

  const recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.lang = "en-US";

  recognition.onresult = (event) => {
  let transcript = "";

  for (let i = event.resultIndex; i < event.results.length; i++) {
    transcript += event.results[i][0].transcript;
  }

  setAnswer((prev) => prev + " " + transcript);
};


  recognition.onend = () => {
    setListening(false);
  };

  recognitionRef.current = recognition;
}, []);


  const loadQuestion = async () => {
    try {
      const res = await api(`/questions/single/${questionId}`);
      setQuestion(res);
    } catch (err) {
      console.error(err);
      alert("Failed to load question");
    }
  };

  const autoSubmit = async () => {
    if (submitting) return;

    try {
      setSubmitting(true);
      await api(`/answers/${questionId}`, {
        method: "POST",
        body: {
          user_answer: answer || "[No answer submitted – time expired]",
        },
      });
      navigate(-1);
    } catch (err) {
      console.error(err);
      alert("Auto submit failed");
    } finally {
      setSubmitting(false);
    }
  };

  useEffect(() => {
  if (!question || timeUp) return;

  if (timeLeft === 0) {
    setTimeUp(true);
    if (recognitionRef.current) {
       recognitionRef.current.stop();
    }
    autoSubmit();
    return;
  }
  const timer = setInterval(() => {
    setTimeLeft((prev) => prev - 1);
  }, 1000);

  return () => clearInterval(timer);
}, [timeLeft, question, timeUp]);

  const startListening = () => {
  if (!recognitionRef.current) {
    alert("Speech recognition not supported in this browser");
    return;
  }

  if (timeUp) return;

  setListening(true);
  recognitionRef.current.start();
};

 const stopListening = () => {
  if (recognitionRef.current) {
    recognitionRef.current.stop();
  }
  setListening(false);
};



  const submitAnswer = async () => {
    if (!answer.trim()) {
      alert("Please write an answer before submitting");
      return;
    }

    try {
      setSubmitting(true);
      await api(`/answers/${questionId}`, {
        method: "POST",
        body: { user_answer: answer },
      });

      navigate(-1); // go back to questions page
    } catch (err) {
      console.error(err);
      alert("Failed to submit answer");
    } finally {
      setSubmitting(false);
    }
  };

  if (!question) return <p>Loading question...</p>;

  return (
    <div className="answer-page">
      <h2>Answer Question</h2>

      <div className="timer-box">
  ⏳ Time Left:{" "}
  <strong className={timeLeft <= 10 ? "danger" : ""}>
    {Math.floor(timeLeft / 60)}:
    {String(timeLeft % 60).padStart(2, "0")}
  </strong>
</div>


      {/* QUESTION DISPLAY */}
      <div className="question-box">
        <h4>Question</h4>
        <p>{question.question_text}</p>
      </div>

      {/* ANSWER INPUT */}
      <div className="answer-box">
        <textarea
          placeholder="Write your answer here..."
          value={answer}
          disabled={timeUp}
          onChange={(e) => setAnswer(e.target.value)}
        />
      </div>

      <div style={{ marginTop: "10px" }}>
  {!listening ? (
  <button
    type="button"
    onClick={startListening}
    disabled={timeUp}
    style={{
      padding: "8px 14px",
      backgroundColor: "#10b981",
      color: "white",
      border: "none",
      borderRadius: "6px",
      cursor: "pointer",
    }}
  >
    🎙️ Start Recording
  </button>
) : (
  <button
    type="button"
    onClick={stopListening}
    style={{
      padding: "8px 14px",
      backgroundColor: "#ef4444",
      color: "white",
      border: "none",
      borderRadius: "6px",
      cursor: "pointer",
    }}
  >
    ⏹ Stop Recording
  </button>
)}

</div>


      {/* ACTIONS */}
      <div className="answer-actions">
        <button onClick={() => navigate(-1)} className="secondary-btn">
          Cancel
        </button>

        <button onClick={submitAnswer} disabled={submitting || timeUp}>
          {timeUp ? "Time Up" :submitting ? "Submitting..." : "Submit Answer"}
        </button>
      </div>
    </div>
  );
}
