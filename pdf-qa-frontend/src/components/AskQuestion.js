import React, { useState } from "react";
import axios from "axios";

const AskQuestion = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleAsk = async () => {
    const formData = new FormData();
    formData.append("filename", "sample.pdf"); // Replace with actual filename
    formData.append("question", question);

    const response = await axios.post("http://127.0.0.1:8000/ask/", formData);
    setAnswer(response.data.answer);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Ask a question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={handleAsk}>Ask</button>
      <p>Answer: {answer}</p>
    </div>
  );
};

export default AskQuestion;
