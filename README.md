# Playlist Recommender

A Streamlit application for music playlist recommendations.

## Running with Docker (macOS)

1. Make sure you have Docker installed on your Mac. You can download it from [Docker's official website](https://www.docker.com/products/docker-desktop).

2. Open Terminal and navigate to the project directory:
   ```bash
   cd /path/to/playlist-reco
   ```

3. Create required directories:
   ```bash
   mkdir -p tokens data
   ```

4. Build the Docker image:
   ```bash
   docker build -t playlist-reco .
   ```

5. Run the Docker container with environment variables and volume mounting:
   ```bash
   docker run -p 8501:8501 \
     --env-file .env \
     -v $(pwd):/app_code \
     -v $(pwd)/tokens:/app/tokens \
     -v $(pwd)/data:/app/data \
     playlist-reco
   ```

   This command:
   - Maps port 8501 for Streamlit
   - Loads environment variables from .env file
   - Mounts your current directory to /app_code in the container
   - Mounts the tokens directory to persist OAuth tokens
   - Mounts the data directory to persist the SQLite database
   - Enables hot-reloading of your code changes

6. Open your web browser and navigate to:
   ```
   http://localhost:8501
   ```

### Volume Mounting Explained

The Docker run command includes three volume mounts:
- `-v $(pwd):/app_code`: Mounts your local project directory to enable hot-reloading
- `-v $(pwd)/tokens:/app/tokens`: Mounts the tokens directory to persist OAuth tokens
- `-v $(pwd)/data:/app/data`: Mounts the data directory to persist the SQLite database

This ensures that:
- Your code changes are immediately reflected
- Your Spotify authorization persists between container restarts
- Your artist data is stored locally and persists between restarts
- You don't need to re-authorize the application each time

### Database Structure

The application uses SQLite to store:
- Artist information (name, popularity, genres)
- Artist images
- Timestamps for data freshness

The database is automatically initialized when the application starts.

### Viewing Docker Logs

To view the application logs, you can use one of these methods:

1. View logs of the running container:
   ```bash
   # Get container ID
   docker ps
   
   # View logs
   docker logs <container_id>
   ```

2. Follow logs in real-time:
   ```bash
   docker logs -f <container_id>
   ```

3. View last N lines of logs:
   ```bash
   docker logs --tail 100 <container_id>
   ```

4. View logs with timestamps:
   ```bash
   docker logs -t <container_id>
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
   - After creating the app, you'll get:
     - Client ID
     - Client Secret
   - Create a `.env` file in the project root with:
     ```
     SPOTIFY_CLIENT_ID=your_client_id
     SPOTIFY_CLIENT_SECRET=your_client_secret
     ```

4. Run the application locally:
   ```bash
   streamlit run main.py
   ```

## Features

- Simple web interface for playlist recommendations
- Artist-based recommendation system
- Modern and responsive design
- Spotify integration for personalized recommendations
- View your top artists from Spotify
- Local database storage for artists
- Persistent data between sessions 