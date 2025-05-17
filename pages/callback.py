import streamlit as st
from lib.spotify_api import SpotifyAPI
from lib.token_manager import TokenManager

# Initialize managers
spotify = SpotifyAPI()
token_manager = TokenManager()

# Get the authorization code from the URL
code = st.experimental_get_query_params().get("code", [None])[0]

if code:
    try:
        # Get and save the token
        token = spotify.get_token(code)
        token_manager.save_token(token)
        st.success("Successfully authorized with Spotify!")
        st.markdown("[Return to Spotify Sync](http://127.0.0.1:8501/spotify_sync)")
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.error("No authorization code received from Spotify") 