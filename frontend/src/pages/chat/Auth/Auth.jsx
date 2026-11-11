import { useState } from "react";
import "./Auth.css";
import { useNavigate } from "react-router-dom";
function Auth() {
  const navigate = useNavigate();
  const [isSignUp, setIsSignUp] = useState(false);

  const [signupData, setSignupData] = useState({
    username: "",
    email: "",
    password: "",
    confirm_password: "",
  });

  const [signupMessage, setSignupMessage] = useState("");
  const [signupError, setSignupError] = useState("");

  const toggleAuth = () => {
    setIsSignUp((prev) => !prev);
  };
  const [loginData, setLoginData] = useState({
    username: "",
    password: "",
  });

  const [loginMessage, setLoginMessage] = useState("");
  const [loginError, setLoginError] = useState("");

  const handleSignupChange = (event) => {
    setSignupData({
      ...signupData,
      [event.target.name]: event.target.value,
    });
  };

  const handleSignup = async (event) => {
    event.preventDefault();

    setSignupMessage("");
    setSignupError("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/auth/register/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(signupData),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setSignupError(
          data.confirm_password?.[0] ||
            data.email?.[0] ||
            data.username?.[0] ||
            data.password?.[0] ||
            "Registration failed."
        );
        return;
      }

      setSignupMessage("Account created successfully.");

      setSignupData({
        username: "",
        email: "",
        password: "",
        confirm_password: "",
      });

      console.log("Registered user:", data.user);
    } catch (error) {
      setSignupError(
        "Could not connect to the server. Is Django running?"
      );
    }
  };
  const handleLoginChange = (event) => {
    setLoginData({
      ...loginData,
      [event.target.name]: event.target.value,
    });
  };

  const handleLogin = async (event) => {
    event.preventDefault();

    setLoginMessage("");
    setLoginError("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/auth/login/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(loginData),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setLoginError("Invalid username or password.");
        return;
      }

      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);

      console.log("Logged in user:", data.user);

      navigate("/chat");

    } catch (error) {
      setLoginError(
        "Could not connect to the server. Is Django running?"
      );
    }
  };

  return (
    <div className={`auth-container ${isSignUp ? "sign-up" : "sign-in"}`}>
      <div className="auth-row">

        {/* SIGN UP */}
        <div className="auth-col auth-sign-up">
          <div className="auth-form-wrapper">
            <form className="auth-form" onSubmit={handleSignup}>
              <span className="auth-tag">New member</span>

              <h1>Sign up.</h1>

              <p className="auth-sub">
                Create your account and get started.
              </p>

              <label htmlFor="signup-username">Username</label>

              <input
                id="signup-username"
                name="username"
                type="text"
                placeholder="Choose a username"
                value={signupData.username}
                onChange={handleSignupChange}
                required
              />

              <label htmlFor="signup-email">Email</label>

              <input
                id="signup-email"
                name="email"
                type="email"
                placeholder="you@example.com"
                value={signupData.email}
                onChange={handleSignupChange}
                required
              />

              <label htmlFor="signup-password">Password</label>

              <input
                id="signup-password"
                name="password"
                type="password"
                placeholder="Create a password"
                value={signupData.password}
                onChange={handleSignupChange}
                required
              />

              <label htmlFor="signup-confirm-password">
                Confirm password
              </label>

              <input
                id="signup-confirm-password"
                name="confirm_password"
                type="password"
                placeholder="Confirm your password"
                value={signupData.confirm_password}
                onChange={handleSignupChange}
                required
              />

              <button type="submit">
                Create account
                <span aria-hidden="true">→</span>
              </button>

              {signupMessage && (
                <p className="auth-success">{signupMessage}</p>
              )}

              {signupError && (
                <p className="auth-error">{signupError}</p>
              )}

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

        {/* SIGN IN */}
        <div className="auth-col auth-sign-in">
          <div className="auth-form-wrapper">
            <form className="auth-form" onSubmit={handleLogin}>
              <span className="auth-tag">Members only</span>

              <h1>Log in.</h1>

              <p className="auth-sub">
                No fluff. Just your account and your work.
              </p>

              <label htmlFor="login-username">Username</label>

<input
  id="login-username"
  name="username"
  type="text"
  placeholder="Your username"
  value={loginData.username}
  onChange={handleLoginChange}
  autoComplete="username"
  required
/>

              <label htmlFor="login-password">Password</label>

<input
  id="login-password"
  name="password"
  type="password"
  placeholder="Your password"
  value={loginData.password}
  onChange={handleLoginChange}
  autoComplete="current-password"
  required
/>
{loginMessage && (
  <p className="auth-success">{loginMessage}</p>
)}

{loginError && (
  <p className="auth-error">{loginError}</p>
)}

              <button type="submit">
                Let me in
                <span aria-hidden="true">→</span>
              </button>

              <div className="auth-links">
                <a href="#">Lost password</a>

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

      <div className="auth-content-row">
        <div className="auth-content-col">
          <div className="auth-content auth-content-sign-in">
            <h2>Welcome</h2>
            <p>Your RAG workspace starts here.</p>
          </div>
        </div>

        <div className="auth-content-col">
          <div className="auth-content auth-content-sign-up">
            <h2>Join RAGLab</h2>
            <p>Build, test and improve your RAG.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Auth;