import React from 'react';

export default function CareerRoadmap({ 
  careerFile, setCareerFile, 
  targetRole, setTargetRole, 
  careerResult, setCareerResult, 
  unifiedFetch, isLoading, clearFeedback, setErrorMessage 
}) {

  const handleCareerRoadmap = async (event) => {
    event.preventDefault();

    if (!careerFile || !targetRole.trim()) {
      setErrorMessage("Please upload a resume and set a target role.");
      return;
    }

    const formData = new FormData();
    formData.append("file", careerFile);
    formData.append("target_role", targetRole.trim());

    const result = await unifiedFetch("/career/generate", {
      method: "POST",
      body: formData,
    });

    if (result) {
      setCareerResult(result);
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

  function renderProjects(title, projects) {
    if (!projects?.length) return null;

    return (
      <div className="result-block">
        <h3>{title}</h3>
        <ul>
          {projects.map((project, index) => (
            <li key={`${title}-${index}`}>
              <strong>{project.title}</strong>
              {project.description && <p>{project.description}</p>}
              {project.technologies?.length > 0 && (
                <p className="technologies-list" style={{fontSize: "0.9em", color: "var(--color-fg-muted)"}}>
                  <em>Tech: {project.technologies.join(', ')}</em>
                </p>
              )}
            </li>
          ))}
        </ul>
      </div>
    );
  }

  function renderWeeklyPlan(title, planItems) {
    if (!planItems?.length) return null;

    return (
      <div className="result-block">
        <h3>{title}</h3>
        <div className="weekly-plan">
          {planItems.map((item, index) => (
            <div key={`week-${index}`} className="weekly-plan-item" style={{marginBottom: "1rem"}}>
              <h4>Week {item.week}: {item.focus}</h4>
              {item.topics?.length > 0 && (
                <ul style={{marginTop: "0.5rem"}}>
                  {item.topics.map((topic, i) => (
                    <li key={`topic-${i}`}>{topic}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  }

  function renderCareerResult() {
    if (!careerResult) {
      return <p className="empty-state">Generate a custom career roadmap that aligns your resume with your target role.</p>;
    }

    return (
      <div className="result-grid">
        <section className="result-card wide">
          <div className="result-block">
            <h3>Target Role</h3>
            <p>{careerResult.target_role}</p>
          </div>
          {renderList("Current Strengths", careerResult.current_strengths)}
          {renderList("Skills to Learn", careerResult.skills_to_learn)}
        </section>
        <section className="result-card">
          {renderProjects("Recommended Projects", careerResult.recommended_projects)}
          {renderList("Certifications", careerResult.recommended_certifications)}
          {renderList("Resources", careerResult.learning_resources)}
          {renderWeeklyPlan("Weekly Plan", careerResult.weekly_plan)}
          {renderList("Estimated Duration", [careerResult.estimated_duration])}
          {renderList("Motivation", [careerResult.motivation])}
        </section>
      </div>
    );
  };

  return (
    <>
      <form className="panel-form" onSubmit={handleCareerRoadmap}>
        <div className="field">
          <label htmlFor="careerFile">Upload Resume PDF</label>
          <input
            id="careerFile"
            type="file"
            accept="application/pdf"
            onChange={(event) => { clearFeedback(); setCareerFile(event.target.files?.[0] || null); }}
          />
        </div>
        <div className="field">
          <label htmlFor="targetRole">Target Role</label>
          <input
            id="targetRole"
            type="text"
            value={targetRole}
            onChange={(event) => { clearFeedback(); setTargetRole(event.target.value); }}
            placeholder="Example: Product Manager, Data Analyst, or Marketing Lead"
          />
        </div>
        <button type="submit" className="primary-button" disabled={isLoading}>
          {isLoading ? "Building…" : "Create Roadmap"}
        </button>
      </form>
      {renderCareerResult()}
    </>
  );
}
