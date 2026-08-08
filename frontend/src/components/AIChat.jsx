import React from 'react';

export default function AIChat({ 
  chatQuestion, setChatQuestion, 
  chatAnswer, setChatAnswer, 
  chatDocFile, setChatDocFile, 
  uploadStatus, setUploadStatus, 
  unifiedFetch, isLoading, clearFeedback, setErrorMessage 
}) {

  const handleDocUpload = async (event) => {
    event?.preventDefault();
    if (!chatDocFile) {
      setErrorMessage("Please select a PDF document to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", chatDocFile);

    const result = await unifiedFetch("/upload", {
      method: "POST",
      body: formData,
    });

    if (result) {
      setUploadStatus(`✓ Document "${result.filename}" uploaded successfully (${result.total_chunks} chunks created). You can now ask questions about it.`);
      setChatDocFile(null);
      setChatAnswer("");
    }
  };

  const handleChat = async (event) => {
    event?.preventDefault();
    if (!chatQuestion.trim()) {
      setErrorMessage("Please enter a question for the AI chat.");
      return;
    }

    const result = await unifiedFetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question: chatQuestion.trim() }),
    });

    if (result) {
      setChatAnswer(result.answer || "No answer returned.");
    }
  };

  return (
    <>
      <form className="panel-form" onSubmit={handleDocUpload}>
        <div className="field">
          <label htmlFor="chatDocFile">Upload a PDF Document for RAG Chat</label>
          <input
            id="chatDocFile"
            type="file"
            accept="application/pdf"
            onChange={(event) => { clearFeedback(); setUploadStatus(""); setChatDocFile(event.target.files?.[0] || null); }}
          />
        </div>
        <button type="submit" className="primary-button" disabled={isLoading}>
          {isLoading ? "Uploading..." : "Upload Document"}
        </button>
      </form>

      {uploadStatus && (
        <div className="notice" style={{
          background: "#f3f7f0",
          color: "var(--muted-sage)",
          borderColor: "var(--muted-sage)",
          borderLeftColor: "var(--muted-sage)"
        }}>
          {uploadStatus}
        </div>
      )}

      <form className="panel-form" onSubmit={handleChat}>
        <div className="field">
          <label htmlFor="chatQuestion">Ask anything about the uploaded document, your resume, goals, or career path</label>
          <textarea
            id="chatQuestion"
            rows="5"
            value={chatQuestion}
            onChange={(event) => { clearFeedback(); setChatQuestion(event.target.value); }}
            placeholder="Type your question here"
          />
        </div>
        <button type="submit" className="primary-button" disabled={isLoading}>
          {isLoading ? "Sending..." : "Send Question"}
        </button>
      </form>

      <section className="result-card">
        <h3>AI Response</h3>
        <p className="response-box">{chatAnswer || "Your answer will appear here after asking a question."}</p>
      </section>
    </>
  );
}
