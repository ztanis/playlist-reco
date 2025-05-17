# Playlist Recommender

A Streamlit application for music playlist recommendations.

## Running with Docker (macOS)

1. Make sure you have Docker installed on your Mac. You can download it from [Docker's official website](https://www.docker.com/products/docker-desktop).

2. Open Terminal and navigate to the project directory:
   ```bash
   cd /path/to/playlist-reco
   ```

3. Build the Docker image:
   ```bash
   docker build -t playlist-reco .
   ```

4. Run the Docker container with environment variables:
   ```bash
   docker run -p 8501:8501 \
     -e SPOTIFY_CLIENT_ID=your_client_id \
     -e SPOTIFY_CLIENT_SECRET=your_client_secret \
     -e SPOTIFY_REDIRECT_URI=http://localhost:8501/callback \
     playlist-reco
   ```

   Alternatively, you can use a .env file:
   ```bash
   docker run -p 8501:8501 --env-file .env playlist-reco
   ```

5. Open your web browser and navigate to:
   ```
   http://localhost:8501
   ```

## Development Setup

1. Install UV package manager:
   ```bash
   pip install uv
   ```

2. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

3. Set up Spotify API credentials:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Log in with your Spotify account
   - Click "Create App"
   - Fill in the app details:
     - App name: Playlist Recommender
     - App description: A music recommendation app
     - Website: http://localhost:8501
     - Redirect URI: http://localhost:8501/callback
   - After creating the app, you'll get:
     - Client ID
     - Client Secret
   - Create a `.env` file in the project root with:
     ```
     SPOTIFY_CLIENT_ID=your_client_id
     SPOTIFY_CLIENT_SECRET=your_client_secret
     SPOTIFY_REDIRECT_URI=http://localhost:8501/callback
     ```

4. Run the application locally:
   ```bash
   streamlit run main.py
   ```

## Features

- Simple web interface for playlist recommendations
- Artist-based recommendation system (coming soon)
- Modern and responsive design
- Spotify integration for personalized recommendations
- View your top artists from Spotify 