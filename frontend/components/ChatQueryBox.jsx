import { useState } from "react";

function ChatQueryBox({ onSubmit, isLoading }) {
  const [question, setQuestion] = useState("");

  async function submitQuestion() {
    const trimmed = question.trim();
    if (!trimmed || isLoading) {
      return;
    }
    setQuestion("");
    await onSubmit(trimmed);
  }

  return (
    <div className="chat-input-row">
      <textarea
        value={question}
        onChange={(event) => setQuestion(event.target.value)}
        placeholder="Example: What is the average order value by month?"
        rows={3}
        onKeyDown={async (event) => {
          if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
            event.preventDefault();
            await submitQuestion();
          }
        }}
      />
      <button type="button" className="primary-button" onClick={submitQuestion} disabled={isLoading}>
        {isLoading ? "Running..." : "Ask Question"}
      </button>
    </div>
  );
}

export default ChatQueryBox;
