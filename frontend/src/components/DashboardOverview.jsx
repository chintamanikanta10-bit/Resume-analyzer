import React from 'react';
import DashboardIcon from './Icons';

export default function DashboardOverview({ resumeResult, atsResult, interviewResult, careerResult, authenticatedUser, FEATURES }) {
  const completedTools = [resumeResult, atsResult, interviewResult, careerResult].filter(Boolean).length;
  const activity = [
    resumeResult && { label: "Resume analysis ready", detail: resumeResult.name || "Structured resume insights generated", icon: "document" },
    atsResult && { label: "ATS review ready", detail: typeof atsResult.ats_score === "undefined" ? "ATS insights generated" : `Match score: ${atsResult.ats_score}%`, icon: "target" },
    interviewResult && { label: "Interview guide ready", detail: "Questions and revision topics generated", icon: "conversation" },
    careerResult && { label: "Career roadmap ready", detail: careerResult.target_role || "Personalized next steps generated", icon: "route" },
  ].filter(Boolean);

  return (
    <>
      <section className="dashboard-welcome">
        <div>
          <p className="eyebrow">Career command center</p>
          <h1>Welcome back{authenticatedUser?.email ? `, ${authenticatedUser.email.split("@")[0]}` : ""}.</h1>
          <p className="hero-copy">Use the sidebar to review your resume, assess role fit, prepare for interviews, and plan the next step in your career.</p>
        </div>
        <div className="welcome-emblem" aria-hidden="true"><DashboardIcon name="spark" size={38} /></div>
      </section>

      <section className="dashboard-stats" aria-label="Workspace overview">
        <article className="dashboard-stat-card">
          <span className="stat-icon"><DashboardIcon name="spark" size={19} /></span>
          <div><span>Available tools</span><strong>{FEATURES.length}</strong><p>Career tools in one workspace</p></div>
        </article>
        <article className="dashboard-stat-card">
          <span className="stat-icon"><DashboardIcon name="target" size={19} /></span>
          <div><span>Completed analyses</span><strong>{completedTools}</strong><p>Results generated this session</p></div>
        </article>
        <article className="dashboard-stat-card">
          <span className="stat-icon"><DashboardIcon name="shield" size={19} /></span>
          <div><span>Workspace status</span><strong>Ready</strong><p>Secure and ready for your next task</p></div>
        </article>
      </section>

      <section className="activity-card" aria-labelledby="activity-title">
        <div className="activity-heading"><div><p className="eyebrow">Recent activity</p><h2 id="activity-title">Your workspace activity</h2></div><span className="activity-status"><span></span> Live session</span></div>
        {activity.length ? (
          <ul className="activity-list">
            {activity.map((item) => <li key={item.label}><span className="activity-icon"><DashboardIcon name={item.icon} size={18} /></span><div><strong>{item.label}</strong><p>{item.detail}</p></div><span className="activity-check"><DashboardIcon name="shield" size={15} /></span></li>)}
          </ul>
        ) : (
          <div className="activity-empty"><span className="activity-icon"><DashboardIcon name="spark" size={19} /></span><div><strong>Your workspace is ready</strong><p>Select a tool from the sidebar to begin an analysis or start a conversation.</p></div></div>
        )}
      </section>
    </>
  );
}
