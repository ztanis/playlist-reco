import streamlit as st
from lib.database import Database
import pandas as pd

st.set_page_config(
    page_title="Saved Artists",
    page_icon="🎧",
    layout="wide"
)

st.title("Saved Artists")

# Initialize database
db = Database()

# Get total number of artists
total_artists = db.get_artist_count()

if total_artists == 0:
    st.info("No artists saved yet. Go to Spotify Sync to load your top artists.")
else:
    st.write(f"Total artists: {total_artists}")
    
    # Get artists from database
    artists = db.get_artists()
    
    # Create a DataFrame for display
    df = pd.DataFrame([
        {
            'Image': f'<img src="{artist["images"][0]["url"]}" width="50">' if artist.get('images') else 'No image',
            'Name': artist['name'],
            'Popularity': artist['popularity'],
            'Genres': ', '.join(artist.get('genres', [])) if artist.get('genres') else 'No genres'
        }
        for artist in artists
    ])
    
    # Display the table
    st.write(df.to_html(escape=False), unsafe_allow_html=True) 