import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Spotify Sync",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 Spotify Sync")
st.write("Connect your Spotify account to get personalized recommendations!")

# Initialize session state for authentication
if 'spotify_auth' not in st.session_state:
    st.session_state.spotify_auth = None
if 'token_info' not in st.session_state:
    st.session_state.token_info = None

def get_spotify_client():
    if st.session_state.spotify_auth is None:
        try:
            auth_manager = SpotifyOAuth(
                client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
                scope='user-top-read',
                cache_handler=spotipy.cache_handler.CacheFileHandler(cache_path='.spotify_caches')
            )
            st.session_state.spotify_auth = auth_manager
        except Exception as e:
            st.error(f"Error initializing Spotify client: {str(e)}")
            return None
    return spotipy.Spotify(auth_manager=st.session_state.spotify_auth)

def display_top_artists(artists):
    st.subheader("Your Top Artists")
    cols = st.columns(3)
    for idx, artist in enumerate(artists):
        with cols[idx % 3]:
            st.image(artist['images'][0]['url'] if artist['images'] else "https://via.placeholder.com/150")
            st.write(f"**{artist['name']}**")
            st.write(f"Popularity: {artist['popularity']}")

if st.button("Sync with Spotify"):
    if not all([os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET'), os.getenv('SPOTIFY_REDIRECT_URI')]):
        st.error("Please set up your Spotify API credentials in the .env file")
    else:
        try:
            sp = get_spotify_client()
            if sp:
                # Get user's top artists
                results = sp.current_user_top_artists(limit=6, time_range='medium_term')
                display_top_artists(results['items'])
        except Exception as e:
            st.error(f"Error fetching data from Spotify: {str(e)}")
            if "No token" in str(e):
                st.info("Please try syncing again to authenticate with Spotify.")

# Display instructions for setting up Spotify API
with st.expander("How to set up Spotify API credentials"):
    st.markdown("""
    1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
    2. Log in with your Spotify account
    3. Click "Create App"
    4. Fill in the app details:
       - App name: Playlist Recommender
       - App description: A music recommendation app
       - Website: http://localhost:8501
       - Redirect URI: http://localhost:8501/callback
    5. After creating the app, you'll get:
       - Client ID
       - Client Secret
    6. Create a `.env` file in the project root with:
       ```
       SPOTIFY_CLIENT_ID=your_client_id
       SPOTIFY_CLIENT_SECRET=your_client_secret
       SPOTIFY_REDIRECT_URI=http://localhost:8501/callback
       ```
    """) 