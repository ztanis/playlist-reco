import os
import openai
import logging
from typing import List, Dict

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

class OpenAIClient:
    def __init__(self):
        logger.info("Initializing OpenAI client")
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        logger.info("OpenAI client initialized")

    def generate_playlist(self, request: str, track_count: int = 10) -> List[Dict[str, str]]:
        """Generate a playlist based on the user's request"""
        try:
            logger.info(f"Generating playlist for request: {request} with {track_count} tracks")
            
            # Log the API call parameters
            logger.info("Making OpenAI API call with parameters:")
            logger.info(f"Model: gpt-3.5-turbo")
            logger.info(f"Temperature: 0.7")
            logger.info(f"Max tokens: 500")
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a music expert that generates playlists based on user requests. Return only a JSON array of exactly {track_count} objects with 'name' and 'artist' fields."},
                    {"role": "user", "content": f"Generate a playlist of exactly {track_count} tracks based on this request: {request}"}
                ],
                temperature=0.7,
                max_tokens=500
            )

            logger.info("Received response from OpenAI API")
            
            # Extract the response content
            content = response.choices[0].message.content
            logger.info(f"Raw response content: {content}")
            
            # Parse the JSON response
            import json
            try:
                tracks = json.loads(content)
                logger.info(f"Successfully parsed JSON response. Number of tracks: {len(tracks)}")
            except json.JSONDecodeError as e:
                logger.info(f"Failed to parse JSON response: {str(e)}")
                raise
            
            # Ensure we have a list of tracks with name and artist
            if not isinstance(tracks, list):
                logger.info("Invalid response format: not a list")
                raise ValueError("Invalid response format")
            
            # Ensure we have the correct number of tracks
            if len(tracks) != track_count:
                logger.info(f"Invalid number of tracks: got {len(tracks)}, expected {track_count}")
                raise ValueError(f"Invalid number of tracks: got {len(tracks)}, expected {track_count}")
                
            for i, track in enumerate(tracks):
                if not isinstance(track, dict) or 'name' not in track or 'artist' not in track:
                    logger.info(f"Invalid track format at index {i}: {track}")
                    raise ValueError("Invalid track format")
                logger.info(f"Valid track {i}: {track['name']} by {track['artist']}")
            
            logger.info("Successfully generated playlist")
            return tracks

        except Exception as e:
            logger.error(f"Error generating playlist: {str(e)}", exc_info=True)
            raise 