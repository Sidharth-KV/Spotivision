
import { useEffect, useState } from "react";
import "./App.css";
import MusicDashboard from "./components/MusicDashboard";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadProfile() {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/auth/me`, {
        credentials: "include",
      });

      if (response.status === 401) {
        setProfile(null);
        return;
      }

      if (!response.ok) {
        throw new Error("Could not retrieve your Spotify profile.");
      }

      const data = await response.json();
      setProfile(data);
    } catch {
      setError("Couldn't connect to FastAPI. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProfile();
  }, []);

  function login() {
    window.location.href = `${API_URL}/auth/login`;
  }

  if (loading) {
    return (
      <main className="page">
        <p className="muted">Connecting to Spotify Analyzer...</p>
      </main>
    );
  }

    return (
      <main className="page">
        <nav className="navbar">
          <a className="brand" href="/">
            <span className="brand-mark">S</span>
            <span>spotify<span className="brand-light">.analyzer</span></span>
          </a>
          <span className="status">
            <span className="status-dot" />
            API connection
          </span>
        </nav>

      <section className="hero">
        <p className="eyebrow">YOUR MUSIC, UNDERSTOOD</p>

        {profile ? (
          <>
            <h1>
              Welcome back,
              <br />
              <span className="accent">
                {profile.display_name || "listener"}.
              </span>
            </h1>

            <p className="subtitle">
              Your Spotify account is connected. Let's explore your listening
              habits.
            </p>

            <>
              <MusicDashboard />
            </>

            {profile.profile_url && (
              <a
                className="secondary-button"
                href={profile.profile_url}
                target="_blank"
                rel="noreferrer"
              >
                View Spotify profile ↗
              </a>
            )}

            <p className="muted next-step">
              Your listening dashboard is the next step.
            </p>
          </>
        ) : (
          <>
            <h1>
              Your music.
              <br />
              <span className="accent">Your patterns.</span>
            </h1>

            <p className="subtitle">
              Explore your listening habits, discover your top artists, and
              understand the music you return to.
            </p>

            <button className="login-button" onClick={login}>
              <span className="spotify-icon">◉</span>
              Continue with Spotify
              <span aria-hidden="true">↗</span>
            </button>

            <p className="muted">
              Connect your Spotify account to get started.
            </p>
          </>
        )}

        {error && <p className="error">{error}</p>}
      </section>

      <footer>
        <span>SPOTIFY ANALYZER</span>
        <span>Built for your listening data.</span>
      </footer>
    </main>
  );
}

export default App;
