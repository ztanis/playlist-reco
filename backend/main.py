from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from lib.database import Database
from lib.spotify_client import SpotifyClient
from lib.openai_client import OpenAIClient
from typing import List, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
db = Database()
spotify_client = SpotifyClient()
openai_client = OpenAIClient()

class Artist(BaseModel):
    id: str
    name: str
    popularity: int
    status: str
    images: List[dict]

class StatusUpdate(BaseModel):
    status: str

class PlaylistRequest(BaseModel):
    request: str

class SyncRequest(BaseModel):
    code: str

@app.get("/api/spotify/auth-url")
async def get_spotify_auth_url():
    try:
        auth_url = spotify_client.get_auth_url()
        return {"auth_url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/spotify/callback")
async def spotify_callback(code: str):
    try:
        # Get access token
        token_data = spotify_client.get_access_token(code)
        if 'error' in token_data:
            raise HTTPException(status_code=400, detail=token_data['error'])

        return {"message": "Token loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/spotify/sync")
async def sync_artists(request: SyncRequest):
    #try:
    existing_artists = db.get_artists()
    logger.info(existing_artists)
    existing_artist_ids = {artist['id'] for artist in existing_artists['artists']}

    # Get access token
    #we still need to have access token
    token_data = spotify_client.get_access_token(request.code)
    if 'error' in token_data:
        raise HTTPException(status_code=400, detail=token_data['error'])

    # Get top artists
    artists_data = spotify_client.get_top_artists()
    if 'error' in artists_data:
        raise HTTPException(status_code=400, detail=artists_data['error'])



    # Add only new artists
    new_artists_count = 0
    for artist in artists_data['items']:
        if artist['id'] not in existing_artist_ids:
            db.add_artist({
                'id': artist['id'],
                'name': artist['name'],
                'popularity': artist['popularity'],
                'images': artist['images']
            })
            new_artists_count += 1
            logger.info(f"Added new artist: {artist['name']}")

    return {
        "message": f"Sync completed: {new_artists_count} new artists added, {len(existing_artists)} existing artists preserved"
    }
    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/artists")
async def get_artists(
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 1000
):
    try:
        result = db.get_artists(status=status, page=page, page_size=page_size)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/artists/{artist_id}/status")
async def update_artist_status(artist_id: str, status_update: StatusUpdate):
    try:
        db.update_artist_status(artist_id, status_update.status)
        return {"message": "Status updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/playlist/generate")
async def generate_playlist(playlist_request: PlaylistRequest):
    try:
        # Generate playlist using OpenAI
        tracks = openai_client.generate_playlist(playlist_request.request)
        
        # Get preview URLs from Spotify
        tracks_with_previews = []
        for track in tracks:
            # Search for the track on Spotify
            search_response = spotify_client.search_track(
                f"{track['name']} {track['artist']}"
            )
            
            if search_response and 'tracks' in search_response:
                items = search_response['tracks'].get('items', [])
                if items:
                    track_info = items[0]
                    tracks_with_previews.append({
                        'name': track['name'],
                        'artist': track['artist'],
                        'preview_url': track_info.get('preview_url')
                    })
        
        return {"tracks": tracks_with_previews}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 