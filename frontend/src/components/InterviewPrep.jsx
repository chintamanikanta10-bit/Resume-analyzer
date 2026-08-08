import React from 'react';

export default function InterviewPrep({ 
  interviewFile, setInterviewFile, 
  interviewJobDescription, setInterviewJobDescription, 
  interviewResult, setInterviewResult, 
  unifiedFetch, isLoading, clearFeedback, setErrorMessage 
}) {

  const handleInterviewPrep = async (event) => {
    event.preventDefault();

    if (!interviewFile || !interviewJobDescription.trim()) {
      setErrorMessage("Please upload a resume and enter the target job description.");
      return;
    }

    const formData = new FormData();
    formData.append("file", interviewFile);
    formData.append("job_description", interviewJobDescription.trim());

    const result = await unifiedFetch("/interview/generate", {
      method: "POST",
      body: formData,
    });

    if (result) {
      setInterviewResult(result);
    }
  };

  function renderList(title, items) {
    if (!items?.length) return null;

    return (
      <div className="result-block">
        <h3>{title}</h3>
        <ul>
          {items.map((item, index) => (
            <li key={`${title}-${index}`}>{item}</li>
          ))}
        </ul>
      </div>
    );
  }

  function renderInterviewQuestionList(title, questions) {
    if (!questions?.length) return null;

    return (
      <div className="result-block">
        <h3>{title}</h3>
        <ul>
          {questions.map((item, index) => (
            <li key={`${title}-${index}`}>
              <div style={{ fontWeight: 700, color: "var(--navy-800)", marginBottom: 6 }}>
                {item.question}
                <span style={{
                  display: "inline-block",
                  marginLeft: 10,
                  padding: "2px 10px",
                  borderRadius: 2,
                  fontSize: "0.75rem",
                  fontWeight: 700,
                  textTransform: "uppercase",
                  letterSpacing: "0.05em",
                  background: item.difficulty?.toLowerCase() === "hard"
                    ? "#fdf3f4"
                    : item.difficulty?.toLowerCase() === "medium"
                    ? "#f8f5ec"
                    : "#f3f7f0",
                  color: item.difficulty?.toLowerCase() === "hard"
                    ? "var(--burgundy)"
                    : item.difficulty?.toLowerCase() === "medium"
                    ? "var(--gold-700)"
                    : "var(--muted-sage)"
                }}>
                  {item.difficulty}
                </span>
              </div>
              {item.answer && (
                <div style={{
                  marginTop: 8,
                  padding: "10px 14px",
                  background: "var(--cream-50)",
                  borderLeft: "2px solid var(--gold-600)",
                  color: "var(--charcoal-700)",
                  lineHeight: 1.7,
                  fontStyle: "italic",
                  fontFamily: "var(--font-serif-body)",
                  fontSize: "1.05rem"
                }}>
                  <strong style={{ color: "var(--navy-700)", fontStyle: "normal", fontFamily: "var(--font-sans)", fontSize: "0.82rem", textTransform: "uppercase", letterSpacing: "0.06em" }}>Suggested Approach: </strong>
                  {item.answer}
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
    );
  }

  function renderInterviewResult() {
    if (!interviewResult) {
      return <p className="empty-state">Generate interview questions and revision topics from your resume.</p>;
    }

    return (
      <div className="result-grid">
        <section className="result-card wide">
          {renderList("Topics to Revise", interviewResult.topics_to_revise)}
          {renderList("Interview Tips", interviewResult.interview_tips)}
        </section>
        <section className="result-card wide">
          {renderInterviewQuestionList("Technical Questions", interviewResult.technical_questions)}
          {renderInterviewQuestionList("HR Questions", interviewResult.hr_questions)}
          {renderInterviewQuestionList("Coding Questions", interviewResult.coding_questions)}
        </section>
      </div>
    );
  };

  return (
    <>
      <form className="panel-form" onSubmit={handleInterviewPrep}>
        <div className="field">
          <label htmlFor="interviewFile">Upload Resume PDF</label>
          <input
            id="interviewFile"
            type="file"
            accept="application/pdf"
            onChange={(event) => { clearFeedback(); setInterviewFile(event.target.files?.[0] || null); }}
          />
        </div>
        <div className="field">
          <label htmlFor="interviewJobDescription">Job Description</label>
          <textarea
            id="interviewJobDescription"
            rows="5"
            value={interviewJobDescription}
            onChange={(event) => { clearFeedback(); setInterviewJobDescription(event.target.value); }}
            placeholder="Paste the job description here"
          />
        </div>
        <button type="submit" className="primary-button" disabled={isLoading}>
          {isLoading ? "Generating…" : "Generate Interview Guide"}
        </button>
      </form>
      {renderInterviewResult()}
    </>
  );
}
