
import secrets
from urllib import response
import requests
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from app.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, FRONTEND_URL

router = APIRouter(prefix="/auth", tags=["Authentication"])

SPOTIFY_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"


@router.get("/login")
def login():
    state = secrets.token_urlsafe(32)

    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": (
            "user-read-private "
            "user-read-email "
            "user-read-recently-played "
            "user-top-read"
        ),
        "state": state,
    }

    from urllib.parse import urlencode

    response = RedirectResponse(
        url=f"{SPOTIFY_AUTHORIZE_URL}?{urlencode(params)}",
        status_code=307,
    )

    response.set_cookie(
        key="spotify_auth_state",
        value=state,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=600,
        path="/",
    )

    return response


@router.get("/callback")
def callback(request: Request):
    error = request.query_params.get("error")

    if error:
        raise HTTPException(
            status_code=400,
            detail=f"Spotify authorization failed: {error}",
        )

    code = request.query_params.get("code")
    state = request.query_params.get("state")
    stored_state = request.cookies.get("spotify_auth_state")
    #diagnostic requirements for state and cookie
    print("Callback received state:", bool(state))
    print("Cookie received:", bool(stored_state))
    print(
        "State matches:",
        bool(state and stored_state and state == stored_state),
    )

    print("\n--- SPOTIFY OAUTH DEBUG ---")
    print("Callback received state:", bool(state))
    print("State cookie received:", bool(stored_state))
    print(
        "State matches:",
        bool(state and stored_state and state == stored_state),
    )
    print("---------------------------\n")

    if not state or not stored_state or state != stored_state:
        raise HTTPException(
            status_code=400,
            detail="Invalid OAuth state",
        )

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Missing authorization code",
        )

    if not state or not stored_state or state != stored_state:
        raise HTTPException(
            status_code=400,
            detail="Invalid OAuth state",
        )

    try:
        if not CLIENT_ID or not CLIENT_SECRET:
            raise ValueError("Missing critical Spotify credentials in environment variables.")
        token_response = requests.post(
            SPOTIFY_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
            auth=(CLIENT_ID, CLIENT_SECRET),
            timeout=15,
        )
    except requests.RequestException:   
        raise HTTPException(
            status_code=502,
            detail="Could not contact Spotify's token service",
        )

    if token_response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Spotify token exchange failed",
        )

    tokens = token_response.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    if not access_token:
        raise HTTPException(
            status_code=502,
            detail="Spotify did not return an access token",
        )

    response = RedirectResponse(
    url=f"{FRONTEND_URL}/",
    status_code=303,
    )

    response.delete_cookie(
        "spotify_auth_state",
        path="/",
        secure=False,
        httponly=True,
        samesite="lax",
    )

    response.set_cookie(
        key="spotify_access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Local HTTP development only
        samesite="lax",
        max_age=tokens.get("expires_in", 3600),
        path="/",
    )
    
    

    if refresh_token:
        response.set_cookie(
            key="spotify_refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,  # Local HTTP development only
            samesite="lax",
            path="/",
        )

    return response
