import streamlit as st
from lib.spotify_api import SpotifyAPI
from lib.token_manager import TokenManager
from lib.database import Database

st.set_page_config(
    page_title="Spotify Sync",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 Spotify Sync++")
st.write("Connect your Spotify account to get personalized recommendations!")

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
            image_url = artist['image_url'] if artist.get('image_url') else "https://via.placeholder.com/80"
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

# Initialize managers
spotify = SpotifyAPI()
token_manager = TokenManager()
db = Database()

# Check if we have a token
token = token_manager.load_token()
if not token:
    st.warning("Please authorize the application first")
    auth_url = spotify.get_auth_url()
    st.markdown(f"[Click here to authorize Spotify]({auth_url})")
else:
    # Set the token for the Spotify API instance
    spotify.token = token
    
    # Add buttons for different actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Load Top Artists"):
            try:
                with st.spinner("Loading your top artists from Spotify..."):
                    # Get artists from Spotify
                    artists = spotify.get_top_artists()
                    # Save to database
                    db.save_artists(artists)
                    st.success(f"Saved {len(artists)} artists to database!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                # If token is invalid, remove it
                if "401" in str(e):
                    token_manager.remove_token()
                    st.experimental_rerun()
    
    with col2:
        if st.button("View Saved Artists"):
            try:
                with st.spinner("Loading artists from database..."):
                    # Get artists from database
                    artists = db.get_artists()
                    st.subheader("Your Saved Artists")
                    display_artists(artists)
            except Exception as e:
                st.error(f"Error loading from database: {str(e)}")

# Display instructions
with st.expander("About this feature"):
    st.markdown("""
    This feature will allow you to:
    - Connect your Spotify account
    - View your top artists
    - Save artists to local database
    - Get personalized recommendations
    - Create custom playlists
    
    Stay tuned for updates!
    """)
