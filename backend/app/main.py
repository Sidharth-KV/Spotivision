
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.spotify.auth import router as auth_router
from app.spotify.client import router as spotify_router

app = FastAPI(title="Spotify Analyzer API")

app.include_router(auth_router)
app.include_router(spotify_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

app.include_router(auth_router)
app.include_router(spotify_router)

@app.get("/")
def home():
    return {
        "message": "Spotify Analyzer API is running",
        "login": "/auth/login",
        "docs": "/docs",
    }


