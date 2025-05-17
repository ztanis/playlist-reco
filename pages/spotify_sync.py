import streamlit as st
import requests
import os
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Spotify Sync",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 Spotify Sync")
st.write("Connect your Spotify account to get personalized recommendations!")

def get_auth_url():
    """
    Get Spotify authorization URL
    """
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    auth_url = "https://accounts.spotify.com/authorize"
    redirect_uri = "http://127.0.0.1:8501/callback"
    scope = "user-top-read"
    
    auth_params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope
    }
    
    return f"{auth_url}?{requests.compat.urlencode(auth_params)}"

def get_top_artists(token):
    """
    Get user's top artists from Spotify
    """
    url = "https://api.spotify.com/v1/me/top/artists"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    params = {
        "limit": 50,
        "time_range": "medium_term"
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        raise Exception(f"Failed to get top artists: {response.text}")

def display_artists(artists):
    """
    Display artists in a table format with images
    """
    # Show total number of artists
    st.write(f"**Total Artists:** {len(artists)}")
    
    # Create header row
    cols = st.columns([1, 3, 1])
    with cols[0]:
        st.write("**Image**")
    with cols[1]:
        st.write("**Artist Name**")
    with cols[2]:
        st.write("**Popularity**")
    
    # Add a divider
    st.markdown("---")
    
    # Display each artist in a row
    for artist in artists:
        cols = st.columns([1, 3, 1])
        with cols[0]:
            # Display smaller image (80x80)
            image_url = artist['images'][0]['url'] if artist['images'] else "https://via.placeholder.com/80"
            st.image(image_url, width=80)
        with cols[1]:
            st.write(f"**{artist['name']}**")
            # Add genres if available
            if artist.get('genres'):
                st.write(f"*{', '.join(artist['genres'][:2])}*")
        with cols[2]:
            # Create a progress bar for popularity
            popularity = artist['popularity']
            st.progress(popularity / 100)
            st.write(f"{popularity}%")
        
        # Add a subtle divider between artists
        st.markdown("---")

# Check if we have a token in session state
if 'spotify_token' not in st.session_state:
    st.warning("Please authorize the application first")
    auth_url = get_auth_url()
    st.markdown(f"[Click here to authorize Spotify]({auth_url})")
else:
    # Add a button to load top artists
    if st.button("Load Top Artists"):
        try:
            with st.spinner("Loading your top artists..."):
                # Get and display top artists
                artists = get_top_artists(st.session_state['spotify_token'])
                st.subheader("Your Top Artists")
                display_artists(artists)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            # If token is invalid, remove it from session state
            if "401" in str(e):
                del st.session_state['spotify_token']
                st.experimental_rerun()

# Display instructions
with st.expander("About this feature"):
    st.markdown("""
    This feature will allow you to:
    - Connect your Spotify account
    - View your top artists
    - Get personalized recommendations
    - Create custom playlists
    
    Stay tuned for updates!
    """)
