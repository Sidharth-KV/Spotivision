
import requests

from fastapi import APIRouter, Cookie, HTTPException, Query

router = APIRouter(tags=["Spotify"])

SPOTIFY_API_URL = "https://api.spotify.com/v1"


def spotify_get(
    endpoint: str,
    access_token: str,
    params: dict | None = None,
):
    try:
        response = requests.get(
            f"{SPOTIFY_API_URL}{endpoint}",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            params=params,
            timeout=15,
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Could not contact Spotify",
        )

    if response.status_code == 401:
        raise HTTPException(
            status_code=401,
            detail="Access token expired or invalid. Log in again.",
        )

    if response.status_code == 403:
        raise HTTPException(
            status_code=403,
            detail="Spotify denied access to this endpoint.",
        )

    if response.status_code == 429:
        raise HTTPException(
            status_code=429,
            detail="Spotify rate limit reached. Try again later.",
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Spotify API returned status {response.status_code}",
        )

    return response.json()


def require_token(token: str | None) -> str:
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not logged in. Visit /auth/login first.",
        )

    return token


@router.get("/auth/me")
def get_profile(
    spotify_access_token: str | None = Cookie(default=None),
):
    token = require_token(spotify_access_token)
    profile = spotify_get("/me", token)

    return {
        "id": profile.get("id"),
        "display_name": profile.get("display_name"),
        "email": profile.get("email"),
        "profile_url": profile.get("external_urls", {}).get("spotify"),
        "images": profile.get("images", []),
    }


@router.get("/spotify/top-tracks")
def get_top_tracks(
    spotify_access_token: str | None = Cookie(default=None),
    time_range: str = Query(
        default="medium_term",
        pattern="^(short_term|medium_term|long_term)$",
    ),
    limit: int = Query(default=10, ge=1, le=50),
):
    token = require_token(spotify_access_token)

    data = spotify_get(
        "/me/top/tracks",
        token,
        params={
            "time_range": time_range,
            "limit": limit,
        },
    )

    return {
        "time_range": time_range,
        "total": data.get("total", 0),
        "tracks": [
            {
                "id": track.get("id"),
                "name": track.get("name"),
                "artists": [
                    artist.get("name")
                    for artist in track.get("artists", [])
                ],
                "album": track.get("album", {}).get("name"),
                "album_image": (
                    track.get("album", {}).get("images", [{}])[0].get("url")
                    if track.get("album", {}).get("images")
                    else None
                ),
                "duration_ms": track.get("duration_ms"),
                "spotify_url": track.get("external_urls", {}).get("spotify"),
            }
            for track in data.get("items", [])
        ],
    }


@router.get("/spotify/top-artists")
def get_top_artists(
    spotify_access_token: str | None = Cookie(default=None),
    time_range: str = Query(
        default="medium_term",
        pattern="^(short_term|medium_term|long_term)$",
    ),
    limit: int = Query(default=10, ge=1, le=50),
):
    token = require_token(spotify_access_token)

    data = spotify_get(
        "/me/top/artists",
        token,
        params={
            "time_range": time_range,
            "limit": limit,
        },
    )

    return {
        "time_range": time_range,
        "total": data.get("total", 0),
        "artists": [
            {
                "id": artist.get("id"),
                "name": artist.get("name"),
                "genres": artist.get("genres", []),
                "image": (
                    artist.get("images", [{}])[0].get("url")
                    if artist.get("images")
                    else None
                ),
                "spotify_url": artist.get("external_urls", {}).get("spotify"),
            }
            for artist in data.get("items", [])
        ],
    }


from datetime import datetime, timezone


@router.get("/spotify/recently-played")
def get_recently_played(
    spotify_access_token: str | None = Cookie(default=None),
    limit: int = Query(default=20, ge=1, le=50),
):
    token = require_token(spotify_access_token)

    data = spotify_get(
        "/me/player/recently-played",
        token,
        params={"limit": limit},
    )

    return {
        "total_returned": len(data.get("items", [])),
        "tracks": [
            {
                "id": item.get("track", {}).get("id"),
                "name": item.get("track", {}).get("name"),
                "artists": [
                    artist.get("name")
                    for artist in item.get("track", {}).get("artists", [])
                ],
                "album": item.get("track", {}).get("album", {}).get("name"),
                "played_at": item.get("played_at"),
                "spotify_url": item.get("track", {}).get(
                    "external_urls", {}
                ).get("spotify"),
            }
            for item in data.get("items", [])
        ],
    }
