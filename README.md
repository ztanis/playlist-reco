# Playlist Recommender

A Streamlit application for music playlist recommendations.

## Running with Docker (macOS)

1. Make sure you have Docker installed on your Mac. You can download it from [Docker's official website](https://www.docker.com/products/docker-desktop).

2. Open Terminal and navigate to the project directory:
   ```bash
   cd /path/to/playlist-reco
   ```

3. Create a tokens directory for OAuth token persistence:
   ```bash
   mkdir -p tokens
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
     playlist-reco
   ```

   This command:
   - Maps port 8501 for Streamlit
   - Loads environment variables from .env file
   - Mounts your current directory to /app_code in the container
   - Mounts the tokens directory to persist OAuth tokens
   - Enables hot-reloading of your code changes

6. Open your web browser and navigate to:
   ```
   http://localhost:8501
   ```

### Volume Mounting Explained

The Docker run command includes two volume mounts:
- `-v $(pwd):/app_code`: Mounts your local project directory to enable hot-reloading
- `-v $(pwd)/tokens:/app/tokens`: Mounts the tokens directory to persist OAuth tokens between container restarts

This ensures that:
- Your code changes are immediately reflected
- Your Spotify authorization persists between container restarts
- You don't need to re-authorize the application each time

### Token Persistence

The application stores OAuth tokens in the `tokens` directory:
- Tokens are saved in `tokens/spotify_token.json`
- The directory is mounted to the container
- Tokens persist between container restarts
- The directory is gitignored for security

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
- Artist-based recommendation system (coming soon)
- Modern and responsive design
- Spotify integration for personalized recommendations
- View your top artists from Spotify 