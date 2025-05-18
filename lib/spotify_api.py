import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SpotifyAPI:
    def __init__(self, token=None):
        self.token = token
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = "http://127.0.0.1:8501/callback"

    def get_auth_url(self):
        """
        Get Spotify authorization URL
        """
        auth_url = "https://accounts.spotify.com/authorize"
        scope = "user-top-read"
        
        auth_params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": scope
        }
        
        return f"{auth_url}?{requests.compat.urlencode(auth_params)}"

    def get_token(self, code):
        """
        Exchange authorization code for access token
        """
        token_url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        response = requests.post(token_url, headers=headers, data=data)
        if response.status_code == 200:
            token_data = response.json()
            return token_data['access_token']
        else:
            raise Exception(f"Failed to get token: {response.text}")

    def get_top_artists(self):
        """
        Get user's top artists from Spotify using pagination
        """
        if not self.token:
            raise Exception("No token available")

        url = "https://api.spotify.com/v1/me/top/artists"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        all_artists = []
        limit = 50  # Maximum allowed by Spotify API
        offset = 0
        
        # Make 4 requests to get up to 200 artists
        for _ in range(4):
            params = {
                "limit": limit,
                "offset": offset,
                "time_range": "long_term"
            }
            
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                artists = response.json()["items"]
                if not artists:  # If no more artists, break
                    break
                all_artists.extend(artists)
                offset += limit
            else:
                raise Exception(f"Failed to get top artists: {response.text}")
        
        return all_artists 