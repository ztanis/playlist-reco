import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json
from pathlib import Path

# Load environment variables
load_dotenv()

# Create tokens directory if it doesn't exist
TOKENS_DIR = Path("tokens")
TOKENS_DIR.mkdir(exist_ok=True)

def save_token(token):
    """
    Save token to a file
    """
    token_file = TOKENS_DIR / "spotify_token.json"
    with open(token_file, "w") as f:
        json.dump({"token": token}, f)

def get_token(code):
    """
    Exchange authorization code for access token
    """
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = "http://127.0.0.1:8501/callback"
    
    # Prepare the request
    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    # Make the request
    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code == 200:
        token_data = response.json()
        # Save token to file immediately
        save_token(token_data['access_token'])
        return token_data['access_token']
    else:
        raise Exception(f"Failed to get token: {response.text}")

# Get the authorization code from the URL
code = st.experimental_get_query_params().get("code", [None])[0]

if code:
    try:
        # Get and save the token
        token = get_token(code)
        st.success("Successfully authorized with Spotify!")
        st.markdown("[Return to Spotify Sync](http://127.0.0.1:8501/spotify_sync)")
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.error("No authorization code received from Spotify") 