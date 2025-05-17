import streamlit as st
import requests
import os
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Spotify Callback",
    page_icon="🎵",
    layout="wide"
)

# Get the authorization code from URL parameters
query_params = st.experimental_get_query_params()
code = query_params.get("code", [None])[0]

if code:
    try:
        # Exchange the code for a token
        token_url = "https://accounts.spotify.com/api/token"
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        headers = {
            "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://127.0.0.1:8501/callback"
        }
        
        response = requests.post(token_url, headers=headers, data=data)
        if response.status_code == 200:
            token_data = response.json()
            # Store the token in session state
            st.session_state['spotify_token'] = token_data['access_token']
            st.success("Successfully authenticated with Spotify!")
            st.markdown("[Return to Spotify Sync](/spotify_sync)")
            st.write(st.write(st.session_state['spotify_token']))
        else:
            st.error(f"Failed to get token: {response.text}")
    except Exception as e:
        st.error(f"Error during authentication: {str(e)}")
else:
    st.error("No authorization code received")
    st.markdown("[Return to Spotify Sync](/spotify_sync)") 