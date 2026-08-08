import React, { useState, Suspense, lazy } from "react";
import "./App.css";
import DashboardIcon from "./components/Icons";
import LoadingSkeleton from "./components/LoadingSkeleton";
import AppFooter from "./components/AppFooter";

const Cover = lazy(() => import("./components/Cover"));
const Auth = lazy(() => import("./components/Auth"));
const DashboardOverview = lazy(() => import("./components/DashboardOverview"));
const AIChat = lazy(() => import("./components/AIChat"));
const ResumeAnalyzer = lazy(() => import("./components/ResumeAnalyzer"));
const ATSAnalyzer = lazy(() => import("./components/ATSAnalyzer"));
const InterviewPrep = lazy(() => import("./components/InterviewPrep"));
const CareerRoadmap = lazy(() => import("./components/CareerRoadmap"));

const FEATURES = [
  "AI Chat",
  "Resume Analyzer",
  "ATS Analyzer",
  "Interview Prep",
  "Career Roadmap",
];

const SIDEBAR_ITEMS = ["Dashboard", ...FEATURES];

const FEATURE_DESCRIPTIONS = {
  "AI Chat": "Ask questions about a resume, a role, or a career path.",
  "Resume Analyzer": "Extract structured details from a candidate resume.",
  "ATS Analyzer": "Compare a resume to a job description and score fit.",
  "Interview Prep": "Create tailored interview questions and prep topics.",
  "Career Roadmap": "Build a step-by-step plan for your next role.",
};

const FEATURE_META = {
  "Dashboard": { icon: "spark", kicker: "Career workspace" },
  "AI Chat": { icon: "spark", kicker: "Ask with context" },
  "Resume Analyzer": { icon: "document", kicker: "Extract key details" },
  "ATS Analyzer": { icon: "target", kicker: "Measure role fit" },
  "Interview Prep": { icon: "conversation", kicker: "Practice with purpose" },
  "Career Roadmap": { icon: "route", kicker: "Plan your next move" },
};

function App() {
  const API_BASE = import.meta.env.VITE_API_BASE || "/api";

  const [view, setView] = useState("cover");
  const [authenticatedUser, setAuthenticatedUser] = useState(null);

  const [activeFeature, setActiveFeature] = useState("Dashboard");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const [chatQuestion, setChatQuestion] = useState("");
  const [chatAnswer, setChatAnswer] = useState("");
  const [chatDocFile, setChatDocFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  const [resumeFile, setResumeFile] = useState(null);
  const [resumeResult, setResumeResult] = useState(null);

  const [atsFile, setAtsFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [atsResult, setAtsResult] = useState(null);

  const [interviewFile, setInterviewFile] = useState(null);
  const [interviewJobDescription, setInterviewJobDescription] = useState("");
  const [interviewResult, setInterviewResult] = useState(null);

  const [careerFile, setCareerFile] = useState(null);
  const [targetRole, setTargetRole] = useState("");
  const [careerResult, setCareerResult] = useState(null);

  const clearFeedback = () => {
    setErrorMessage("");
  };

  const navigateTo = (feature) => {
    setActiveFeature(feature);
    setErrorMessage("");
    setIsSidebarOpen(false);
  };

  const unifiedFetch = async (path, options = {}) => {
    setIsLoading(true);
    setErrorMessage("");

    const requestUrl = path.startsWith("http") ? path : `${API_BASE}${path}`;

    try {
      const response = await fetch(requestUrl, {
        credentials: "include",
        ...options,
      });

      const text = await response.text();
      let result = null;
      try {
        result = text ? JSON.parse(text) : null;
      } catch (_parseErr) {
        result = null;
      }

      if (!response.ok) {
        const msg =
          result?.detail ||
          result?.message ||
          (response.status === 502 ? "Backend server is not reachable. Please start the backend server." : null) ||
          (response.status === 500 ? "Internal server error." : null) ||
          response.statusText ||
          `Server error (HTTP ${response.status})`;
        throw new Error(msg);
      }

      return result;
    } catch (error) {
      let msg = error?.message || "Network request failed";
      if (msg === "Failed to fetch" || msg.toLowerCase().includes("load failed")) {
        msg = "Cannot connect to the server. Please check if both frontend and backend are running.";
      }
      setErrorMessage(msg);
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    setAuthenticatedUser(null);
    setErrorMessage("");
    setView("cover");
  };

  const renderActivePanel = () => {
    switch (activeFeature) {
      case "Resume Analyzer":
        return <ResumeAnalyzer resumeFile={resumeFile} setResumeFile={setResumeFile} resumeResult={resumeResult} setResumeResult={setResumeResult} unifiedFetch={unifiedFetch} isLoading={isLoading} clearFeedback={clearFeedback} setErrorMessage={setErrorMessage} />;
      case "ATS Analyzer":
        return <ATSAnalyzer atsFile={atsFile} setAtsFile={setAtsFile} jobDescription={jobDescription} setJobDescription={setJobDescription} atsResult={atsResult} setAtsResult={setAtsResult} unifiedFetch={unifiedFetch} isLoading={isLoading} clearFeedback={clearFeedback} setErrorMessage={setErrorMessage} />;
      case "Interview Prep":
        return <InterviewPrep interviewFile={interviewFile} setInterviewFile={setInterviewFile} interviewJobDescription={interviewJobDescription} setInterviewJobDescription={setInterviewJobDescription} interviewResult={interviewResult} setInterviewResult={setInterviewResult} unifiedFetch={unifiedFetch} isLoading={isLoading} clearFeedback={clearFeedback} setErrorMessage={setErrorMessage} />;
      case "Career Roadmap":
        return <CareerRoadmap careerFile={careerFile} setCareerFile={setCareerFile} targetRole={targetRole} setTargetRole={setTargetRole} careerResult={careerResult} setCareerResult={setCareerResult} unifiedFetch={unifiedFetch} isLoading={isLoading} clearFeedback={clearFeedback} setErrorMessage={setErrorMessage} />;
      default:
        return <AIChat chatQuestion={chatQuestion} setChatQuestion={setChatQuestion} chatAnswer={chatAnswer} setChatAnswer={setChatAnswer} chatDocFile={chatDocFile} setChatDocFile={setChatDocFile} uploadStatus={uploadStatus} setUploadStatus={setUploadStatus} unifiedFetch={unifiedFetch} isLoading={isLoading} clearFeedback={clearFeedback} setErrorMessage={setErrorMessage} />;
    }
  };

  return (
    <div className="app-shell">
      <Suspense fallback={<LoadingSkeleton />}>
        {view === "cover" && <Cover setView={setView} />}
        {view === "login" && <Auth type="login" setView={setView} unifiedFetch={unifiedFetch} setAuthenticatedUser={setAuthenticatedUser} isLoading={isLoading} errorMessage={errorMessage} setErrorMessage={setErrorMessage} />}
        {view === "register" && <Auth type="register" setView={setView} unifiedFetch={unifiedFetch} setAuthenticatedUser={setAuthenticatedUser} isLoading={isLoading} errorMessage={errorMessage} setErrorMessage={setErrorMessage} />}
      </Suspense>

      {view === "app" && (
        <div className="dashboard-layout">
          <aside className={isSidebarOpen ? "app-sidebar is-open" : "app-sidebar"} aria-label="Application navigation">
            <div className="sidebar-brand">
              <span className="dashboard-brand-mark"><DashboardIcon name="spark" size={18} /></span>
              <span>InsightHub</span>
            </div>
            <nav className="sidebar-nav" aria-label="Career tools">
              {SIDEBAR_ITEMS.map((item) => (
                <button
                  key={item}
                  type="button"
                  className={item === activeFeature ? "sidebar-link active" : "sidebar-link"}
                  onClick={() => navigateTo(item)}
                >
                  <DashboardIcon name={item === "Dashboard" ? "home" : FEATURE_META[item].icon} size={19} />
                  <span>{item}</span>
                </button>
              ))}
            </nav>
            <div className="sidebar-footer">
              <span className="sidebar-footer-label">InsightHub workspace</span>
              <button type="button" className="sidebar-link logout-link" onClick={handleLogout}>
                <DashboardIcon name="logout" size={19} />
                <span>Logout</span>
              </button>
            </div>
          </aside>

          <div className="dashboard-content">
            <header className="dashboard-topbar">
              <button
                className="sidebar-toggle"
                type="button"
                onClick={() => setIsSidebarOpen((open) => !open)}
                aria-label="Toggle navigation"
                aria-expanded={isSidebarOpen}
              >
                <DashboardIcon name={isSidebarOpen ? "close" : "menu"} size={20} />
              </button>

              <nav className="topbar-breadcrumb" aria-label="Breadcrumb">
                <button
                  type="button"
                  className={activeFeature === "Dashboard" ? "breadcrumb-link breadcrumb-link--current" : "breadcrumb-link"}
                  onClick={() => navigateTo("Dashboard")}
                >
                  Dashboard
                </button>
                {activeFeature !== "Dashboard" && (
                  <>
                    <span className="breadcrumb-sep" aria-hidden="true">›</span>
                    <span className="breadcrumb-current">{activeFeature}</span>
                  </>
                )}
              </nav>

              <div className="dashboard-topbar-actions">
                <span className="secure-status"><DashboardIcon name="shield" size={15} /> Private workspace</span>
                {authenticatedUser && (
                  <div className="user-bar">
                    <span className="user-avatar">{authenticatedUser.email.charAt(0).toUpperCase()}</span>
                    <span className="user-email">{authenticatedUser.email}</span>
                  </div>
                )}
              </div>
            </header>

            <div className="dashboard-main panel-fade-in" key={activeFeature}>
              {activeFeature === "Dashboard" ? (
                <Suspense fallback={<LoadingSkeleton />}>
                  <DashboardOverview
                    resumeResult={resumeResult}
                    atsResult={atsResult}
                    interviewResult={interviewResult}
                    careerResult={careerResult}
                    authenticatedUser={authenticatedUser}
                    FEATURES={FEATURES}
                  />
                </Suspense>
              ) : (
                <main className="panel">
                  <div className="panel-heading">
                    <div className="panel-feature-icon">
                      <DashboardIcon name={FEATURE_META[activeFeature].icon} size={22} />
                    </div>
                    <div>
                      <p>{FEATURE_META[activeFeature].kicker}</p>
                      <h2>{activeFeature}</h2>
                      <p className="panel-description">{FEATURE_DESCRIPTIONS[activeFeature]}</p>
                    </div>
                  </div>
                  {errorMessage && <div className="notice notice-error">{errorMessage}</div>}
                  <Suspense fallback={<LoadingSkeleton />}>
                    {renderActivePanel()}
                  </Suspense>
                </main>
              )}
            </div>

            <AppFooter />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
