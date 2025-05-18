from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from lib.database import Database
from lib.spotify_client import SpotifyClient
from lib.openai_client import OpenAIClient
from typing import List, Optional, Dict
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

class GenerateRequest(BaseModel):
    request: str
    track_count: int = 10

class UploadRequest(BaseModel):
    tracks: List[Dict[str, str]]
    name: str

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
        
        return {"message": "Token loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/spotify/sync")
async def sync_artists(request: SyncRequest):
    #try:
    existing_artists = db.get_artists()
    logger.info(existing_artists)
    existing_artist_ids = {artist['id'] for artist in existing_artists['artists']}


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
async def generate_playlist(request: GenerateRequest):
    try:
        tracks = openai_client.generate_playlist(request.request, request.track_count)
        return {"tracks": tracks}
    except Exception as e:
        logger.error(f"Error generating playlist: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/playlist/upload")
async def upload_to_spotify(request: UploadRequest):
    try:
        # Search for each track and collect their Spotify IDs
        track_ids = []
        for track in request.tracks:
            track_id = await spotify_client.search_track(track['name'], track['artist'])
            if track_id:
                track_ids.append(track_id)
            else:
                logger.warning(f"Could not find track: {track['name']} by {track['artist']}")

        if not track_ids:
            raise HTTPException(status_code=404, detail="No tracks found on Spotify")

        # Create playlist and add tracks
        playlist_url = await spotify_client.create_playlist(request.name, track_ids)
        return {"playlist_url": playlist_url}
    except Exception as e:
        logger.error(f"Error uploading to Spotify: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 