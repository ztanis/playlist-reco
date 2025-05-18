import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
from .token_manager import TokenManager

logger = logging.getLogger(__name__)

class SpotifyClient:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
        self.token_manager = TokenManager()
        self._init_spotify()

    def _init_spotify(self):
        """Initialize Spotify client with current token"""
        token_data = self.token_manager.get_token()
        if token_data and 'access_token' in token_data:
            self.sp = spotipy.Spotify(auth=token_data['access_token'])
        else:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope='playlist-modify-public playlist-modify-private user-top-read'
            ))

    def get_auth_url(self):
        """Get Spotify authorization URL"""
        auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope='playlist-modify-public playlist-modify-private user-top-read'
        )
        return auth_manager.get_authorize_url()

    def get_access_token(self, code):
        """Exchange authorization code for access token"""
        try:
            auth_manager = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope='playlist-modify-public playlist-modify-private user-top-read'
            )
            token_info = auth_manager.get_access_token(code)
            logger.info(f"save token with {token_info}")
            if token_info:
                self.token_manager.save_token(token_info)
                self._init_spotify()
            return token_info
        except Exception as e:
            logger.error(f"Error getting access token: {str(e)}")
            return {'error': str(e)}

    def get_top_artists(self, limit=50):
        """Get user's top artists"""
        try:
            self._init_spotify()  # Refresh token if needed
            all_artists = []
            batch_size = 50  # Spotify's maximum limit
            total_artists = 200  # Total number of artists we want
            offset = 0

            while len(all_artists) < total_artists:
                # Get batch of artists with same parameters as original call
                logger.info(f"Getting batch of artists from {offset} to {offset + batch_size}")
                batch = self.sp.current_user_top_artists(
                    limit=batch_size,
                    time_range='long_term',
                    offset=offset,
                )
                
                if not batch.get('items'):
                    break
                    
                all_artists.extend(batch['items'])
                offset += batch_size

                # If we got less than the batch size, we've reached the end
                if len(batch['items']) < batch_size:
                    break

            # Return in the same format as spotipy
            return {
                'items': all_artists[:total_artists],
                'total': len(all_artists[:total_artists]),
                'limit': batch_size,
                'offset': 0
            }
        except Exception as e:
            logger.error(f"Error getting top artists: {str(e)}")
            return {'error': str(e)}

    def create_playlist(self, name, description=""):
        """Create a new playlist"""
        try:
            self._init_spotify()  # Refresh token if needed
            user = self.sp.current_user()
            return self.sp.user_playlist_create(
                user=user['id'],
                name=name,
                description=description,
                public=True
            )
        except Exception as e:
            logger.error(f"Error creating playlist: {str(e)}")
            return {'error': str(e)}

    def search_track(self, name, artist):
        """Search for a track"""
        try:
            self._init_spotify()  # Refresh token if needed
            query = f"track:{name} artist:{artist}"
            return self.sp.search(query, type='track', limit=1)
        except Exception as e:
            logger.error(f"Error searching track: {str(e)}")
            return {'error': str(e)}

    def add_tracks_to_playlist(self, playlist_id, track_uris):
        """Add tracks to a playlist"""
        try:
            self._init_spotify()  # Refresh token if needed
            return self.sp.playlist_add_items(playlist_id, track_uris)
        except Exception as e:
            logger.error(f"Error adding tracks to playlist: {str(e)}")
            return {'error': str(e)} 