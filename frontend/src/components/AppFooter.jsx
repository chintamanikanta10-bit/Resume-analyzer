import DashboardIcon from "./Icons";

export default function AppFooter({ variant = "app" }) {
  const isCover = variant === "cover";

  return (
    <footer className={isCover ? "app-footer app-footer--cover" : "app-footer"}>
      <div className="app-footer-brand">
        <span className="app-footer-mark">
          <DashboardIcon name="spark" size={16} />
        </span>
        <div>
          <strong>{isCover ? "AI Career Assistant" : "InsightHub"}</strong>
          <p>AI-powered career guidance for ambitious professionals.</p>
        </div>
      </div>
      <div className="app-footer-meta">
        <span>© 2025 {isCover ? "AI Career Assistant" : "InsightHub"}</span>
        <span className="app-footer-divider" aria-hidden="true">·</span>
        <span>All rights reserved</span>
      </div>
    </footer>
  );
}
