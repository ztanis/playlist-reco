import os
import openai
import logging
from typing import List, Dict
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('openai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info(f"openi version: {openai.version.VERSION}") 

class Track(BaseModel):
    name: str = Field(..., description="The name of the track")
    artist: str = Field(..., description="The name of the artist")

class PlaylistResponse(BaseModel):
    name: str = Field(..., description="A short, catchy name for the playlist")
    tracks: List[Track] = Field(..., min_items=1, max_items=50)

class OpenAIClient:
    def __init__(self):
        logger.info("Initializing OpenAI client")
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        logger.info("OpenAI client initialized")

    def generate_playlist(self, request: str, track_count: int = 10, liked_artists_names: list[str] = None) -> Dict[str, any]:
        """Generate a playlist based on the user's request"""
        try:
            logger.info(f"Generating playlist for request: {request} with {track_count} tracks")
            
            # Log the API call parameters
            logger.info("Making OpenAI API call with parameters:")
            logger.info(f"Model: gpt-3.5-turbo")
            logger.info(f"Temperature: 0.7")
            logger.info(f"Max tokens: 2000")

            if liked_artists_names is not None:
                liked_artists_message = f"Consider the following artists as favorites: {', '.join(liked_artists_names)}"
            else:
                liked_artists_message = ""

            messages = [
                    {
                        "role": "system",
                        "content": f"""You are a music expert that generates playlists based on user requests.
                        You must return a valid JSON object with a playlist name and exactly {track_count} tracks.
                        The playlist name should be short, catchy, and reflect the theme of the playlist.
                        Each track must have a name and artist.
                        Make sure the tracks are diverse and match the user's request.

                        If favourite artists are provided consider them in the playlist, but only if they are relevant to the request.
                        
                        Important: Ensure the response is a complete, valid JSON object.
                        The response must match this exact schema:
                        {{
                            "name": "string (max 50 chars)",
                            "tracks": [
                                {{
                                    "name": "string",
                                    "artist": "string"
                                }}
                            ]
                        }}"""
                    },
                    {
                        "role": "user",
                        "content": f"""
                        Generate a playlist of exactly {track_count} tracks based on this request: {request}. 
                        {liked_artists_message}"""
                    }
                ]
            
            logger.info(f"Request for openai: {messages}")

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            logger.info("Received response from OpenAI API")
            
            # Extract the response content
            content = response.choices[0].message.content
            logger.info(f"Raw response content: {content}")
            
            # Parse the JSON response using Pydantic
            try:
                # Ensure the response is complete JSON
                if not content.strip().endswith('}'):
                    raise ValueError("Incomplete JSON response")
                
                playlist_data = PlaylistResponse.model_validate_json(content)
                tracks = [track.model_dump() for track in playlist_data.tracks]
                tracks = tracks[:track_count]
                logger.info(f"Successfully parsed JSON response. Number of tracks: {len(tracks)}")
            except Exception as e:
                logger.info(f"Failed to parse JSON response: {str(e)}")
                raise ValueError(f"Invalid response format: {str(e)}")
            
            # Ensure we have the correct number of tracks
            if len(tracks) != track_count:
                logger.info(f"Invalid number of tracks: got {len(tracks)}, expected {track_count}")
                raise ValueError(f"Invalid number of tracks: got {len(tracks)}, expected {track_count}")
            
            logger.info("Successfully generated playlist")
            return {
                "name": playlist_data.name,
                "tracks": tracks
            }

        except Exception as e:
            logger.error(f"Error generating playlist: {str(e)}", exc_info=True)
            raise 