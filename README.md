# Spotivision

Beautiful stranger(hi lol), this is a full-stack Spotify analytics application that connects to a user's Spotify account and presents personalized music data through an interactive dashboard. Built with FastAPI, React, and the Spotify Web API.

## Features

- **Spotify OAuth 2.0 Authentication** — Connect your Spotify account through the Spotify authorization flow.
- **User Profile** — View your connected Spotify account and profile information.
- **Top Tracks** — Explore your most-listened-to tracks across different time ranges.
- **Top Artists** — View your top artists, including artist images and available genre information.
- **Recently Played** — Browse your recently played tracks and playback timestamps.
- **Interactive Dashboard** — Explore track rankings, album artwork, artist information, and direct links to Spotify.

## Tech Stack

**Frontend**
- React
- Vite
- JavaScript
- CSS

**Backend**
- Python
- FastAPI
- Spotipy / Spotify API integration
- Requests

**Authentication and Integration**
- Spotify Web API
- OAuth 2.0

## Architecture

The application uses a React frontend to display music analytics and a FastAPI backend to handle Spotify authentication and API requests.

```text
User
  |
  v
React + Vite Dashboard
  |
  v
FastAPI Backend
  |
  v
Spotify Web API
  |
  v
Music Data
(Top Tracks, Top Artists,
Recently Played, Profile)
  |
  v
Interactive Dashboard
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- Node.js and npm
- A Spotify account
- A Spotify Developer application

### 1. Clone the Repository

```bash
git clone https://github.com/Sidharth-KV/Spotify-Analyzer.git
cd Spotify-Analyzer
```

### 2. Configure Spotify API Credentials

Create an application in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).

Configure the application's redirect URI to match the backend callback URL used by your local setup.

Create a `.env` file in the backend directory and configure the credentials required by the application:

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://127.0.0.1:8000/auth/callback
FRONTEND_URL=http://127.0.0.1:5173
```

Use the variable names expected by your backend configuration. Never commit your client secret or other credentials to GitHub.

### 3. Start the Backend

Open a terminal and navigate to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

Install the backend dependencies using the repository's dependency file, if present:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The backend should be available at:

- API: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs

### 4. Start the Frontend

Open another terminal and navigate to the frontend directory:

```bash
cd dashboard
```

Install the dependencies and start the development server:

```bash
npm install
npm run dev
```

Open the frontend at:

http://127.0.0.1:5173

Keep the frontend and backend URLs consistent with the application's CORS and OAuth configuration.

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /auth/login` | Initiates Spotify authentication |
| `GET /auth/callback` | Handles the Spotify OAuth callback |
| `GET /auth/me` | Retrieves the connected user's profile |
| `GET /spotify/top-tracks` | Retrieves the user's top tracks |
| `GET /spotify/top-artists` | Retrieves the user's top artists |
| `GET /spotify/recently-played` | Retrieves recently played tracks |

The top-tracks and top-artists endpoints support time-range selection. Refer to the interactive API documentation at `/docs` for the available parameters and response schemas.

## Security Notes

- Store Spotify credentials in environment variables.
- Keep `.env` files and other sensitive credentials out of version control.
- Use the configured OAuth redirect URI consistently during local development.
- Authenticated API requests rely on the application's Spotify authentication flow.

## Future Improvements

- Persistent listening-history storage and synchronization.
- Automated access-token refresh handling.
- Listening trends and temporal analytics.
- Additional visualizations and personalized music insights.

## Author

**Sidharth K Vinod**(couldn't be me :O)

[GitHub Repository](https://github.com/Sidharth-KV/Spotivision)
