import React, { useState } from "react";
import DashboardIcon from "./Icons";

const AUTH_FEATURES = [
  { icon: "document", text: "Structured resume extraction" },
  { icon: "target", text: "ATS-style role fit scoring" },
  { icon: "conversation", text: "Tailored interview preparation" },
  { icon: "route", text: "Personalized career roadmaps" },
];

export default function Auth({
  type,
  setView,
  unifiedFetch,
  setAuthenticatedUser,
  isLoading,
  errorMessage,
  setErrorMessage,
}) {
  const isLogin = type === "login";

  const [authEmail, setAuthEmail] = useState("");
  const [authPassword, setAuthPassword] = useState("");
  const [authConfirmPassword, setAuthConfirmPassword] = useState("");
  const [authMessage, setAuthMessage] = useState("");

  const handleLogin = async (event) => {
    event?.preventDefault();
    setAuthMessage("");
    setErrorMessage("");

    if (!authEmail.trim() || !authPassword.trim()) {
      setAuthMessage("Please enter both email and password.");
      return;
    }

    const result = await unifiedFetch("/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: authEmail.trim(),
        password: authPassword,
      }),
    });

    if (result) {
      // Store JWT token so protected API requests can use it
      if (result.access_token) {
        localStorage.setItem("access_token", result.access_token);
      }

      setAuthenticatedUser({
        email: result.email,
      });

      setAuthMessage(result.message || "Login successful.");
      setView("app");
    }
  };

  const handleRegister = async (event) => {
    event?.preventDefault();
    setAuthMessage("");
    setErrorMessage("");

    if (
      !authEmail.trim() ||
      !authPassword.trim() ||
      !authConfirmPassword.trim()
    ) {
      setAuthMessage("Please complete all registration fields.");
      return;
    }

    if (authPassword !== authConfirmPassword) {
      setAuthMessage("Passwords do not match.");
      return;
    }

    const result = await unifiedFetch("/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: authEmail.trim(),
        password: authPassword,
      }),
    });

    if (result) {
      // Store JWT token returned after registration
      if (result.access_token) {
        localStorage.setItem("access_token", result.access_token);
      }

      setAuthenticatedUser({
        email: result.email,
      });

      setAuthMessage(result.message || "Account created successfully.");
      setView("app");
    }
  };

  return (
    <div className="auth-shell full-bleed">
      <div className="auth-layout">
        <aside className="auth-brand-panel" aria-hidden="true">
          <div className="auth-brand-top">
            <span className="auth-brand-mark">
              <DashboardIcon name="spark" size={22} />
            </span>

            <span className="auth-brand-name">InsightHub</span>
          </div>

          <h2>Your career workspace, powered by AI.</h2>

          <p>
            Upload, analyze, and prepare — all in one secure dashboard designed
            for modern professionals.
          </p>

          <ul className="auth-feature-list">
            {AUTH_FEATURES.map((item) => (
              <li key={item.text}>
                <span className="auth-feature-icon">
                  <DashboardIcon name={item.icon} size={17} />
                </span>

                {item.text}
              </li>
            ))}
          </ul>
        </aside>

        <div className="auth-form-panel">
          <button
            className="auth-back-link text-button"
            type="button"
            onClick={() => {
              setView("cover");
              setAuthMessage("");
              setErrorMessage("");
            }}
          >
            ← Back to home
          </button>

          <div className="auth-card">
            <p className="eyebrow">
              {isLogin ? "Welcome back" : "Create your account"}
            </p>

            <h1>
              {isLogin ? "Sign in to continue" : "Register for access"}
            </h1>

            <p className="hero-copy">
              {isLogin
                ? "Enter your credentials to access your career workspace."
                : "Create an account to unlock resume analysis, ATS scoring, and interview prep."}
            </p>

            {authMessage && (
              <div className="notice notice-loading">
                {authMessage}
              </div>
            )}

            {errorMessage && (
              <div className="notice notice-error">
                {errorMessage}
              </div>
            )}

            <form
              className="panel-form"
              onSubmit={isLogin ? handleLogin : handleRegister}
            >
              <div className="field">
                <label htmlFor="authEmail">Email address</label>

                <input
                  id="authEmail"
                  type="email"
                  value={authEmail}
                  onChange={(event) => {
                    setAuthEmail(event.target.value);
                    setAuthMessage("");
                    setErrorMessage("");
                  }}
                  placeholder="you@example.com"
                />
              </div>

              <div className="field">
                <label htmlFor="authPassword">Password</label>

                <input
                  id="authPassword"
                  type="password"
                  value={authPassword}
                  onChange={(event) => {
                    setAuthPassword(event.target.value);
                    setAuthMessage("");
                    setErrorMessage("");
                  }}
                  placeholder="Enter your password"
                />
              </div>

              {!isLogin && (
                <div className="field">
                  <label htmlFor="authConfirmPassword">
                    Confirm password
                  </label>

                  <input
                    id="authConfirmPassword"
                    type="password"
                    value={authConfirmPassword}
                    onChange={(event) => {
                      setAuthConfirmPassword(event.target.value);
                      setAuthMessage("");
                      setErrorMessage("");
                    }}
                    placeholder="Repeat your password"
                  />
                </div>
              )}

              <button
                type="submit"
                className="primary-button"
                disabled={isLoading}
              >
                {isLogin ? "Sign in" : "Create account"}
              </button>
            </form>

            <button
              className="text-button"
              type="button"
              onClick={() => {
                setView(isLogin ? "register" : "login");
                setAuthMessage("");
                setErrorMessage("");
              }}
            >
              {isLogin
                ? "Don't have an account? Register"
                : "Already have an account? Sign in"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}