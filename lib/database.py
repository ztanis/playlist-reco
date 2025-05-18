import sqlite3
from pathlib import Path
import json
from datetime import datetime

class Database:
    def __init__(self):
        self.db_dir = Path("/data")
        self.db_dir.mkdir(exist_ok=True)
        self.db_path = self.db_dir / "playlist_reco.db"
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create artists table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS artists (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    popularity INTEGER,
                    genres TEXT,
                    image_url TEXT,
                    status TEXT DEFAULT 'not_ranked',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create artist_images table for multiple images
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS artist_images (
                    artist_id TEXT,
                    url TEXT,
                    width INTEGER,
                    height INTEGER,
                    FOREIGN KEY (artist_id) REFERENCES artists(id),
                    PRIMARY KEY (artist_id, url)
                )
            """)
            
            conn.commit()

    def save_artists(self, artists):
        """Save artists to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            now = datetime.utcnow().isoformat()
            
            for artist in artists:
                # Save main artist data
                cursor.execute("""
                    INSERT OR REPLACE INTO artists 
                    (id, name, popularity, genres, image_url, status, updated_at)
                    VALUES (?, ?, ?, ?, ?, COALESCE((SELECT status FROM artists WHERE id = ?), 'not_ranked'), ?)
                """, (
                    artist['id'],
                    artist['name'],
                    artist['popularity'],
                    json.dumps(artist.get('genres', [])),
                    artist['images'][0]['url'] if artist.get('images') else None,
                    artist['id'],  # For COALESCE to check existing status
                    now
                ))
                
                # Save all images
                if artist.get('images'):
                    cursor.execute("DELETE FROM artist_images WHERE artist_id = ?", (artist['id'],))
                    for image in artist['images']:
                        cursor.execute("""
                            INSERT INTO artist_images (artist_id, url, width, height)
                            VALUES (?, ?, ?, ?)
                        """, (
                            artist['id'],
                            image['url'],
                            image.get('width'),
                            image.get('height')
                        ))
            
            conn.commit()

    def get_artists(self, limit=50, offset=0, status=None):
        """Retrieve artists from the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT a.*, GROUP_CONCAT(ai.url) as image_urls
                FROM artists a
                LEFT JOIN artist_images ai ON a.id = ai.artist_id
            """
            
            params = []
            if status:
                query += " WHERE a.status = ?"
                params.append(status)
                
            query += """
                GROUP BY a.id
                ORDER BY a.popularity DESC
                LIMIT ? OFFSET ?
            """
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            
            columns = [description[0] for description in cursor.description]
            artists = []
            
            for row in cursor.fetchall():
                artist = dict(zip(columns, row))
                if artist['genres']:
                    artist['genres'] = json.loads(artist['genres'])
                if artist['image_urls']:
                    artist['images'] = [{'url': url} for url in artist['image_urls'].split(',')]
                artists.append(artist)
            
            return artists

    def get_artist_count(self, status=None):
        """Get total number of artists in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute("SELECT COUNT(*) FROM artists WHERE status = ?", (status,))
            else:
                cursor.execute("SELECT COUNT(*) FROM artists")
            return cursor.fetchone()[0]

    def update_artist_status(self, artist_id, status):
        """Update the status of an artist"""
        valid_statuses = ['not_ranked', 'like', 'dislike', 'neutral']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE artists 
                SET status = ?, updated_at = ?
                WHERE id = ?
            """, (status, datetime.utcnow().isoformat(), artist_id))
            conn.commit() 