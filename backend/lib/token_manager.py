import json
import os
from pathlib import Path
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TokenManager:
    def __init__(self):
        self.tokens_dir = Path("/app/tokens")
        self.token_file = self.tokens_dir / "spotify_token.json"
        self._ensure_tokens_dir()

    def _ensure_tokens_dir(self):
        """Ensure the tokens directory exists"""
        if not self.tokens_dir.exists():
            self.tokens_dir.mkdir(parents=True)
            logger.info(f"Created tokens directory at {self.tokens_dir.absolute()}")

    def save_token(self, token_data: dict):
        """Save token data to file"""
        try:
            # Add timestamp for token expiration tracking
            token_data['timestamp'] = datetime.now().isoformat()
            
            with open(self.token_file, 'w') as f:
                json.dump(token_data, f)
            logger.info(f"Saved token to {self.token_file}")
        except Exception as e:
            logger.error(f"Error saving token: {str(e)}")
            raise

    def get_token(self) -> dict:
        """Get the current token, checking for expiration"""
        try:
            if not self.token_file.exists():
                logger.error(f"Token file not found at {self.token_file}")
                return None

            with open(self.token_file, 'r') as f:
                token_data = json.load(f)

            # Check if token is expired (Spotify tokens typically expire in 1 hour)
            if 'timestamp' in token_data:
                token_time = datetime.fromisoformat(token_data['timestamp'])
                if datetime.now() - token_time > timedelta(minutes=55):  # Refresh 5 minutes before expiry
                    logger.info("Token is expired or about to expire")
                    return None

            return token_data
        except Exception as e:
            logger.error(f"Error reading token: {str(e)}")
            return None

    def clear_token(self):
        """Clear the stored token"""
        try:
            if self.token_file.exists():
                self.token_file.unlink()
                logger.info("Cleared token file")
        except Exception as e:
            logger.error(f"Error clearing token: {str(e)}")
            raise 