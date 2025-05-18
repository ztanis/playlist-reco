import os
import openai
import logging
from typing import List, Dict, Any

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

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be set")
        openai.api_key = self.api_key

    def generate_playlist(self, request: str) -> List[Dict[str, Any]]:
        logger.info(f"Generating playlist for request: {request}")
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a music expert. Given a playlist request, 
                        generate a list of 20 songs that match the request. For each song, 
                        provide the song name and artist name. Format your response as a 
                        JSON array of objects with 'name' and 'artist' fields.
                        
                        You will receive a list of songs that the user likes. Consider the description of the playlist more important than the list of sonts.
                
                        """
                    },
                    {
                        "role": "user",
                        "content": request
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse the response to get the list of tracks
            tracks = eval(response.choices[0].message.content)
            logger.info(f"Generated {len(tracks)} tracks")
            
            return tracks
            
        except Exception as e:
            logger.error(f"Error generating playlist: {str(e)}")
            raise 