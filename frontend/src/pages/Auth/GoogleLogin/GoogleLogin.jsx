import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "./GoogleLogin.css";

function GoogleLogin() {
  const googleButtonRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const initializeGoogle = () => {
      if (!window.google || !googleButtonRef.current) {
        return;
      }

      window.google.accounts.id.initialize({
        client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,

        callback: async (response) => {
          try {
            const backendResponse = await fetch(
              "http://127.0.0.1:8000/api/auth/google/",
              {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  credential: response.credential,
                }),
              }
            );

            const data = await backendResponse.json();

            if (!backendResponse.ok) {
              console.error("Google login failed:", data);
              return;
            }

            localStorage.setItem(
              "access_token",
              data.access
            );

            localStorage.setItem(
              "refresh_token",
              data.refresh
            );

            console.log("Google user:", data.user);

            navigate("/chat");
          } catch (error) {
            console.error(
              "Could not connect to Django:",
              error
            );
          }
        },
      });

      window.google.accounts.id.renderButton(
        googleButtonRef.current,
        {
          theme: "outline",
          size: "large",
          text: "continue_with",
          shape: "rectangular",
          width: 320,
        }
      );
    };

    if (window.google) {
      initializeGoogle();
    } else {
      const interval = setInterval(() => {
        if (window.google) {
          clearInterval(interval);
          initializeGoogle();
        }
      }, 100);

      return () => clearInterval(interval);
    }
  }, [navigate]);

  return (
    <div
      ref={googleButtonRef}
      className="google-login"
    />
  );
}

export default GoogleLogin;