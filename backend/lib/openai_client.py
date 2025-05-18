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
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def generate_playlist(self, request: str) -> List[Dict[str, str]]:
        """Generate a playlist based on the user's request"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a music expert that generates playlists based on user requests. Return only a JSON array of objects with 'name' and 'artist' fields."},
                    {"role": "user", "content": f"Generate a playlist based on this request: {request}"}
                ],
                temperature=0.7,
                max_tokens=500
            )

            # Extract the response content
            content = response.choices[0].message.content
            
            # Parse the JSON response
            import json
            tracks = json.loads(content)
            
            # Ensure we have a list of tracks with name and artist
            if not isinstance(tracks, list):
                raise ValueError("Invalid response format")
                
            for track in tracks:
                if not isinstance(track, dict) or 'name' not in track or 'artist' not in track:
                    raise ValueError("Invalid track format")
            
            return tracks

        except Exception as e:
            logger.error(f"Error generating playlist: {str(e)}")
            raise 