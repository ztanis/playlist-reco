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

4. Run the Docker container:
   ```bash
   docker run -p 8501:8501 playlist-reco
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

3. Run the application locally:
   ```bash
   streamlit run main.py
   ```

## Features

- Simple web interface for playlist recommendations
- Artist-based recommendation system (coming soon)
- Modern and responsive design 