# Artist Ranking App

A web application for ranking your favorite artists, built with React and FastAPI.

## Project Structure

```
.
├── backend/           # FastAPI backend
│   ├── main.py       # Main FastAPI application
│   ├── Dockerfile    # Backend Docker configuration
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── App.tsx
│   │   └── ...
│   ├── Dockerfile    # Frontend Docker configuration
│   ├── nginx.conf    # Nginx configuration
│   └── package.json
└── docker-compose.yml
```

## Spotify Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Add `http://localhost/callback` to the Redirect URIs in your app settings
4. Copy the Client ID and Client Secret
5. Create a `.env` file in the project root with:
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

## Running with Docker

1. Make sure you have Docker and Docker Compose installed on your system.

2. Build and start the containers:
```bash
docker-compose up --build
```

3. Access the application:
   - Web Interface: http://localhost
   - API Documentation: http://localhost:8000/docs
   - API Base URL: http://localhost:8000/api

To stop the containers:
```bash
docker-compose down
```

## API Endpoints

The API is available at http://localhost:8000/api with the following endpoints:

- `GET /api/artists` - Get all artists
  - Query parameters:
    - `status`: Filter by status (optional)
    - Example: http://localhost:8000/api/artists?status=like

- `PUT /api/artists/{artist_id}/status` - Update artist status
  - Path parameters:
    - `artist_id`: The Spotify artist ID
  - Body:
    ```json
    {
      "status": "like" | "dislike" | "neutral" | "not_ranked"
    }
    ```
  - Example: http://localhost:8000/api/artists/123/status

- `GET /api/spotify/auth-url` - Get Spotify authorization URL
  - Returns the URL to redirect users to for Spotify authentication

- `GET /api/spotify/callback` - Handle Spotify OAuth callback
  - Query parameters:
    - `code`: The authorization code from Spotify
  - Loads the user's top artists and saves them to the database

You can explore and test all API endpoints using the Swagger UI at http://localhost:8000/docs

## Development Setup

### Backend

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Run the backend server:
```bash
uvicorn main:app --reload
```

The backend will be available at http://localhost:8000

### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

The frontend will be available at http://localhost:3000

## Features

- Connect with Spotify to load your top artists
- View list of artists
- Filter artists by ranking status
- Update artist rankings (Like, Dislike, Neutral, Not Ranked)
- Real-time updates
- Responsive design

## Technologies Used

- Frontend:
  - React
  - TypeScript
  - CSS Modules
  - Nginx
- Backend:
  - FastAPI
  - SQLAlchemy
  - Pydantic
  - Spotify Web API
- Infrastructure:
  - Docker
  - Docker Compose 