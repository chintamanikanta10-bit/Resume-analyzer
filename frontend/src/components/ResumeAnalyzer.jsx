import React from 'react';

export default function ResumeAnalyzer({ 
  resumeFile, setResumeFile, 
  resumeResult, setResumeResult, 
  unifiedFetch, isLoading, clearFeedback, setErrorMessage 
}) {

  const handleResumeAnalyze = async (event) => {
    event.preventDefault();
    if (!resumeFile) {
      setErrorMessage("Please upload a PDF resume for analysis.");
      return;
    }

    const formData = new FormData();
    formData.append("file", resumeFile);

    const result = await unifiedFetch("/resume/analyze", {
      method: "POST",
      body: formData,
    });

    if (result) {
      setResumeResult(result);
    }
  };

  function renderChip(label) {
    return <span className="pill" key={label}>{label}</span>;
  }

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

  function renderResumeResult() {
    if (!resumeResult) {
      return <p className="empty-state">Upload a resume to receive structured insights.</p>;
    }

    return (
      <div className="result-grid">
        <section className="result-card">
          <div className="result-header">
            <h3>{resumeResult.name || "Candidate"}</h3>
            <p className="meta">{resumeResult.email} · {resumeResult.phone} · {resumeResult.location}</p>
          </div>
          {resumeResult.skills?.length > 0 && <div className="chips">{resumeResult.skills.map(renderChip)}</div>}
          {renderList("Certifications", resumeResult.certifications)}
          {renderList("Achievements", resumeResult.achievements)}
        </section>
        <section className="result-card">
          {renderList("Education", resumeResult.education?.map((item) => `${item.degree}, ${item.institution} · ${item.score}`))}
          {renderList("Experience", resumeResult.experience?.map((item) => `${item.role} • ${item.company} · ${item.duration}`))}
          {renderList("Projects", resumeResult.projects?.map((item) => `${item.title}: ${item.description}`))}
        </section>
      </div>
    );
  }

  return (
    <>
      <form className="panel-form" onSubmit={handleResumeAnalyze}>
        <div className="field">
          <label htmlFor="resumeFile">Upload Resume PDF</label>
          <input
            id="resumeFile"
            type="file"
            accept="application/pdf"
            onChange={(event) => { clearFeedback(); setResumeFile(event.target.files?.[0] || null); }}
          />
        </div>
        <button type="submit" className="primary-button" disabled={isLoading}>
          {isLoading ? "Analyzing…" : "Analyze Resume"}
        </button>
      </form>
      {renderResumeResult()}
    </>
  );
}
