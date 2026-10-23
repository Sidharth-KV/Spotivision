
import { useEffect, useState } from "react";
import { apiGet } from "../api";

function formatDuration(ms) {
  if (typeof ms !== "number") return "—";

  const minutes = Math.floor(ms / 60000);
  const seconds = Math.floor((ms % 60000) / 1000);

  return `${minutes}:${String(seconds).padStart(2, "0")}`;
}

export default function MusicDashboard() {
  const [timeRange, setTimeRange] = useState("medium_term");
  const [tracks, setTracks] = useState([]);
  const [artists, setArtists] = useState([]);
  const [recent, setRecent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadDashboard() {
      setLoading(true);
      setError("");

      try {
        const [trackData, artistData, recentData] =
          await Promise.all([
            apiGet(
              `/spotify/top-tracks?time_range=${timeRange}&limit=10`
            ),
            apiGet(
              `/spotify/top-artists?time_range=${timeRange}&limit=10`
            ),
            apiGet("/spotify/recently-played?limit=10"),
          ]);

        if (!cancelled) {
          setTracks(trackData.tracks);
          setArtists(artistData.artists);
          setRecent(recentData.tracks);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message || "Failed to load music data.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadDashboard();

    return () => {
      cancelled = true;
    };
  }, [timeRange]);

  if (loading) {
    return (
      <main className="dashboard-content">
        <p className="muted">Loading your listening data...</p>
      </main>
    );
  }

  if (error) {
    return (
      <main className="dashboard-content">
        <h2>Couldn't load your music</h2>
        <p className="error">{error}</p>
        <p className="muted">
          If your session has expired, reconnect your Spotify account.
        </p>
        <button
          className="login-button"
          onClick={() => {
            window.location.href =
              "http://127.0.0.1:8000/auth/login";
          }}
        >
          Reconnect Spotify
        </button>
      </main>
    );
  }

  return (
    <main className="dashboard-content">
      <header className="dashboard-heading">
        <div>
          <p className="eyebrow">YOUR LISTENING DATA</p>
          <h1>Your music<span className="accent">.</span></h1>
          <p className="subtitle">
            A snapshot of the artists and tracks in your rotation.
          </p>
        </div>

        <label className="range-picker">
          <span>Top items period</span>
          <select
            value={timeRange}
            onChange={(event) => setTimeRange(event.target.value)}
          >
            <option value="short_term">Last 4 weeks</option>
            <option value="medium_term">Last 6 months</option>
            <option value="long_term">Last 12 months</option>
          </select>
        </label>
      </header>

      <section className="music-section">
        <h2>Top tracks</h2>
        {tracks.length === 0 ? (
          <p className="muted">No top tracks were returned.</p>
        ) : (
          <div className="music-grid">
            {tracks.map((track, index) => (
              <a
                className="music-card"
                href={track.spotify_url || "#"}
                target="_blank"
                rel="noreferrer"
                key={track.id || `${track.name}-${index}`}
              >
                {track.album_image ? (
                  <img
                    className="cover"
                    src={track.album_image}
                    alt={`${track.album} cover`}
                  />
                ) : (
                  <div className="cover cover-placeholder">♫</div>
                )}

                <span className="rank">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <strong>{track.name}</strong>
                <span className="muted">
                  {track.artists.join(", ")}
                </span>
                <span className="duration">
                  {formatDuration(track.duration_ms)}
                </span>
              </a>
            ))}
          </div>
        )}
      </section>

      <section className="music-section">
        <h2>Top artists</h2>
        {artists.length === 0 ? (
          <p className="muted">No top artists were returned.</p>
        ) : (
          <div className="artist-grid">
            {artists.map((artist, index) => (
              <a
                className="artist-card"
                href={artist.spotify_url || "#"}
                target="_blank"
                rel="noreferrer"
                key={artist.id || `${artist.name}-${index}`}
              >
                {artist.image ? (
                  <img
                    className="artist-image"
                    src={artist.image}
                    alt={artist.name}
                  />
                ) : (
                  <div className="artist-image artist-placeholder">
                    ♫
                  </div>
                )}

                <span className="muted">
                  ARTIST {String(index + 1).padStart(2, "0")}
                </span>
                <strong>{artist.name}</strong>
                <span className="muted">
                  {artist.genres.slice(0, 2).join(" · ") ||
                    "Genres unavailable"}
                </span>
              </a>
            ))}
          </div>
        )}
      </section>

      <section className="music-section">
        <h2>Recently played</h2>
        {recent.length === 0 ? (
          <p className="muted">
            No recent listening history was returned.
          </p>
        ) : (
          <div className="recent-list">
            {recent.map((track, index) => (
              <a
                className="recent-row"
                href={track.spotify_url || "#"}
                target="_blank"
                rel="noreferrer"
                key={`${track.id || track.name}-${track.played_at || index}`}
              >
                <span className="recent-index">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <span className="recent-track">{track.name}</span>
                <span className="muted">
                  {track.artists.join(", ")}
                </span>
                <time className="muted">
                  {track.played_at
                    ? new Date(track.played_at).toLocaleString()
                    : ""}
                </time>
              </a>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
    