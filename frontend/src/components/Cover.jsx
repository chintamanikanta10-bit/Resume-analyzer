import React from "react";
import DashboardIcon from "./Icons";
import AppFooter from "./AppFooter";

const FEATURES = [
  { icon: "spark", title: "AI Chat", desc: "Ask contextual questions about resumes, roles, and career paths." },
  { icon: "document", title: "Resume Analyzer", desc: "Extract skills, experience, education, and project insights instantly." },
  { icon: "target", title: "ATS Analyzer", desc: "Compare your resume with job descriptions and receive fit-based scores." },
  { icon: "conversation", title: "Interview Prep", desc: "Generate tailored questions, topics, and answers for your next role." },
  { icon: "route", title: "Career Roadmap", desc: "Build a step-by-step plan toward your target position." },
];

const STEPS = [
  { num: "01", title: "Upload Resume", desc: "Add your PDF to start structured extraction and analysis." },
  { num: "02", title: "Add Job Context", desc: "Paste a job description or target role for relevant feedback." },
  { num: "03", title: "Review Insights", desc: "Receive ATS scoring, gap analysis, and tailored suggestions." },
  { num: "04", title: "Prepare with AI", desc: "Get interview questions, prep topics, and a career roadmap." },
];

export default function Cover({ setView }) {
  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  return (
    <div className="cover-shell full-bleed">
      <div className="cover-wrapper">
        <header className="cover-nav">
          <div className="brand-shell brand-shell--icon-only" aria-label="AI Career Assistant">
            <span className="brand-mark brand-mark--icon">
              <DashboardIcon name="spark" size={18} />
            </span>
          </div>
          <div className="cover-links">
            <button type="button" className="text-button" onClick={() => scrollToSection("features")}>Features</button>
            <button type="button" className="text-button" onClick={() => scrollToSection("how-it-works")}>How it Works</button>
          </div>
          <button className="primary-button" type="button" onClick={() => setView("login")}>Get Started</button>
        </header>

        <section className="cover-hero">
          <div className="cover-hero-intro">
            <span className="eyebrow">AI-Powered Career Assistant</span>
            <h1>Turn your resume into a clear path to your next opportunity.</h1>
            <p className="hero-copy">
              Upload your resume, compare it with job descriptions, and unlock tailored interview prep and roadmap guidance — all in one polished workspace.
            </p>
            <div className="hero-actions">
              <button className="primary-button" type="button" onClick={() => setView("register")}>Create Account</button>
              <button className="secondary-button" type="button" onClick={() => scrollToSection("how-it-works")}>See How It Works</button>
            </div>
            <div className="cover-trust-bar" aria-label="Platform highlights">
              <div className="trust-item">
                <span className="trust-icon"><DashboardIcon name="spark" size={17} /></span>
                <div><strong>5</strong><span>Career tools</span></div>
              </div>
              <div className="trust-item">
                <span className="trust-icon"><DashboardIcon name="shield" size={17} /></span>
                <div><strong>Secure</strong><span>Private workspace</span></div>
              </div>
              <div className="trust-item">
                <span className="trust-icon"><DashboardIcon name="target" size={17} /></span>
                <div><strong>AI-driven</strong><span>Actionable insights</span></div>
              </div>
            </div>
          </div>

          <div className="hero-spotlight">
            <div className="hero-spotlight-card">
              <div className="spotlight-header">
                <span className="spotlight-icon"><DashboardIcon name="document" size={22} /></span>
                <div>
                  <span className="spotlight-label">Workspace preview</span>
                  <h3>Everything for modern career growth</h3>
                </div>
              </div>
              <ul>
                <li>
                  <span className="spotlight-bullet"><DashboardIcon name="spark" size={14} /></span>
                  <div>
                    <strong>Instant clarity</strong>
                    <span>Extract key skills, experience, and structure from your resume in seconds.</span>
                  </div>
                </li>
                <li>
                  <span className="spotlight-bullet"><DashboardIcon name="target" size={14} /></span>
                  <div>
                    <strong>Smarter targeting</strong>
                    <span>Measure fit against job descriptions and sharpen your application strategy.</span>
                  </div>
                </li>
                <li>
                  <span className="spotlight-bullet"><DashboardIcon name="conversation" size={14} /></span>
                  <div>
                    <strong>Confidence building</strong>
                    <span>Prepare for interviews with tailored questions and next-step guidance.</span>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </section>

        <section id="features" className="cover-features">
          <div className="section-heading">
            <span className="section-eyebrow">Built for focused progress</span>
            <h2>One dashboard for every stage of your career journey.</h2>
          </div>
          <div className="feature-cards feature-cards--five">
            {FEATURES.map((feature) => (
              <article key={feature.title} className="feature-card">
                <span className="feature-card-icon"><DashboardIcon name={feature.icon} size={20} /></span>
                <h3>{feature.title}</h3>
                <p>{feature.desc}</p>
              </article>
            ))}
          </div>
        </section>

        <section id="how-it-works" className="cover-how-it-works">
          <div className="section-heading">
            <span className="section-eyebrow">Simple workflow</span>
            <h2>From upload to opportunity in four steps.</h2>
          </div>
          <div className="how-grid">
            {STEPS.map((step) => (
              <div key={step.num} className="how-step">
                <span className="step-number">{step.num}</span>
                <h4>{step.title}</h4>
                <p>{step.desc}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="cover-cta">
          <div className="cover-cta-content">
            <p className="eyebrow">Ready to begin?</p>
            <h2>Start building your career advantage today.</h2>
            <p className="hero-copy">Create a free account and access resume analysis, ATS scoring, interview prep, and more.</p>
          </div>
          <div className="cover-cta-actions">
            <button className="primary-button" type="button" onClick={() => setView("register")}>Create Free Account</button>
            <button className="text-button text-button--underlined" type="button" onClick={() => setView("login")}>Sign in</button>
          </div>
        </section>

        <AppFooter variant="cover" />
      </div>
    </div>
  );
}
