import React from 'react';

export default function ATSAnalyzer({ 
  atsFile, setAtsFile, 
  jobDescription, setJobDescription, 
  atsResult, setAtsResult, 
  unifiedFetch, isLoading, clearFeedback, setErrorMessage 
}) {

  const handleAtsAnalyze = async (event) => {
    event.preventDefault();

    if (!atsFile || !jobDescription.trim()) {
      setErrorMessage("Please provide both a resume PDF and the job description.");
      return;
    }

    const formData = new FormData();
    formData.append("file", atsFile);
    formData.append("job_description", jobDescription.trim());

    const result = await unifiedFetch("/ats/analyze", {
      method: "POST",
      body: formData,
    });

    if (result) {
      setAtsResult(result);
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

  function renderAtsResult() {
    if (!atsResult) {
      return <p className="empty-state">Upload a resume and enter the job description to get an ATS score and feedback.</p>;
    }

    return (
      <div className="result-grid">
        <section className="result-card wide">
          <div className="stat-grid">
            <div className="stat-card">
              <span>ATS Score</span>
              <strong>{atsResult.ats_score}%</strong>
            </div>
            <div className="stat-card">
              <span>Skill Match</span>
              <strong>{atsResult.skill_match_percentage}%</strong>
            </div>
          </div>
          <div className="result-block">
            <h3>Overall Feedback</h3>
            <p>{atsResult.overall_feedback}</p>
          </div>
        </section>
        <section className="result-card">
          {renderList("Strengths", atsResult.strengths)}
          {renderList("Weaknesses", atsResult.weaknesses)}
          {renderList("Missing Skills", atsResult.missing_skills)}
          {renderList("Recommendations", atsResult.recommendations)}
        </section>
      </div>
    );
  };

  return (
    <>
      <form className="panel-form" onSubmit={handleAtsAnalyze}>
        <div className="field">
          <label htmlFor="atsFile">Upload Resume PDF</label>
          <input
            id="atsFile"
            type="file"
            accept="application/pdf"
            onChange={(event) => { clearFeedback(); setAtsFile(event.target.files?.[0] || null); }}
          />
        </div>
        <div className="field">
          <label htmlFor="jobDescription">Job Description</label>
          <textarea
            id="jobDescription"
            rows="5"
            value={jobDescription}
            onChange={(event) => { clearFeedback(); setJobDescription(event.target.value); }}
            placeholder="Paste the job description here"
          />
        </div>
        <button type="submit" className="primary-button" disabled={isLoading}>
          {isLoading ? "Reviewing…" : "Review with ATS"}
        </button>
      </form>
      {renderAtsResult()}
    </>
  );
}
