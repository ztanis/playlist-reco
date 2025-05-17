import streamlit as st

st.set_page_config(
    page_title="Playlist Recommender",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 Playlist Recommender")
st.write("Welcome to the Playlist Recommender app!")

# Add a simple input field
user_input = st.text_input("Enter your favorite artist:", "Taylor Swift")

if user_input:
    st.write(f"Looking for recommendations similar to {user_input}...")
    # Placeholder for future recommendation logic
    st.info("Recommendation feature coming soon!") 