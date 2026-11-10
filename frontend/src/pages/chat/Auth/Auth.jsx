import { useState } from "react";
import "./Auth.css";

function Auth() {
  const [isSignUp, setIsSignUp] = useState(false);

  const toggleAuth = () => {
    setIsSignUp((prev) => !prev);
  };

  return (
    <div className={`auth-container ${isSignUp ? "sign-up" : "sign-in"}`}>

      {/* =========================
          FORM SECTION
      ========================= */}

      <div className="auth-row">

        {/* SIGN UP FORM */}
        <div className="auth-col auth-sign-up">
          <div className="auth-form-wrapper">

            <form className="auth-form" onSubmit={(e) => e.preventDefault()}>

              <span className="auth-tag">New member</span>

              <h1>Sign up.</h1>

              <p className="auth-sub">
                Create your account and get started.
              </p>

              <label htmlFor="signup-email">
                Email
              </label>

              <input
                id="signup-email"
                type="email"
                placeholder="you@example.com"
                autoComplete="email"
              />

              <label htmlFor="signup-password">
                Password
              </label>

              <input
                id="signup-password"
                type="password"
                placeholder="Create a password"
                autoComplete="new-password"
              />

              <label htmlFor="signup-confirm-password">
                Confirm password
              </label>

              <input
                id="signup-confirm-password"
                type="password"
                placeholder="Confirm your password"
                autoComplete="new-password"
              />

              <button type="submit">
                Create account
                <span aria-hidden="true">→</span>
              </button>

              <div className="auth-links">
                <span>Already have an account?</span>

                <button
                  type="button"
                  className="auth-link-button"
                  onClick={toggleAuth}
                >
                  Sign in
                </button>
              </div>

            </form>

          </div>
        </div>


        {/* SIGN IN FORM */}
        <div className="auth-col auth-sign-in">
          <div className="auth-form-wrapper">

            <form className="auth-form" onSubmit={(e) => e.preventDefault()}>

              <span className="auth-tag">Members only</span>

              <h1>Log in.</h1>

              <p className="auth-sub">
                No fluff. Just your account and your work.
              </p>

              <label htmlFor="login-email">
                Email
              </label>

              <input
                id="login-email"
                type="email"
                placeholder="you@example.com"
                autoComplete="username"
              />

              <label htmlFor="login-password">
                Password
              </label>

              <input
                id="login-password"
                type="password"
                placeholder="Top secret"
                autoComplete="current-password"
              />

              <button type="submit">
                Let me in
                <span aria-hidden="true">→</span>
              </button>

              <div className="auth-links">

                <a href="#">
                  Lost password
                </a>

                <button
                  type="button"
                  className="auth-link-button"
                  onClick={toggleAuth}
                >
                  Join instead
                </button>

              </div>

            </form>

          </div>
        </div>

      </div>


      {/* =========================
          ANIMATION / CONTENT SECTION
      ========================= */}

      <div className="auth-content-row">

        {/* SIGN IN SIDE */}
        <div className="auth-content-col">

          <div className="auth-content auth-content-sign-in">

            <h2>
              Welcome
            </h2>

            <p>
              Your RAG workspace starts here.
            </p>

          </div>

        </div>


        {/* SIGN UP SIDE */}
        <div className="auth-content-col">

          <div className="auth-content auth-content-sign-up">

            <h2>
              Join RAGLab
            </h2>

            <p>
              Build, test and improve your RAG.
            </p>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Auth;