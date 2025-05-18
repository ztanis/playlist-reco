import sqlite3
import json
from datetime import datetime
import os
from typing import List, Optional
import logging
from sqlalchemy import text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("Database initialized!!!!!")
class Database:
    def __init__(self, db_path="data/artists.db"):
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
        logger.info(f"Database initialized at {db_path}")

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Create artists table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            popularity INTEGER,
            status TEXT DEFAULT 'not_ranked',
            images TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.conn.commit()
        logger.info("Database tables created/verified")

    def add_artist(self, artist_data):
        cursor = self.conn.cursor()
        
        # Convert images to JSON string
        images_json = json.dumps(artist_data.get('images', []))
        
        cursor.execute('''
        INSERT OR REPLACE INTO artists (id, name, popularity, images, last_updated)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            artist_data['id'],
            artist_data['name'],
            artist_data.get('popularity', 0),
            images_json,
            datetime.now().isoformat()
        ))
        
        self.conn.commit()
        logger.info(f"Added/updated artist: {artist_data['name']} (ID: {artist_data['id']})")

    def get_artist(self, artist_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM artists WHERE id = ?', (artist_id,))
        row = cursor.fetchone()
        
        if row:
            logger.info(f"Retrieved artist: {row['name']} (ID: {artist_id})")
            return self._row_to_dict(row)
        logger.info(f"Artist not found: {artist_id}")
        return None

    def get_artists(self, status: Optional[str] = None, page: int = 1, page_size: int = 20) -> dict:
        cursor = self.conn.cursor()
        
        # Get total count
        if status:
            cursor.execute('SELECT COUNT(*) FROM artists WHERE status = ?', (status,))
        else:
            cursor.execute('SELECT COUNT(*) FROM artists')
        total_count = cursor.fetchone()[0]
        
        # Get paginated and sorted results
        offset = (page - 1) * page_size
        if status:
            cursor.execute('''
                SELECT * FROM artists 
                WHERE status = ? 
                ORDER BY popularity DESC 
                LIMIT ? OFFSET ?
            ''', (status, page_size, offset))
        else:
            cursor.execute('''
                SELECT * FROM artists 
                ORDER BY popularity DESC 
                LIMIT ? OFFSET ?
            ''', (page_size, offset))
        
        rows = cursor.fetchall()
        artists = [self._row_to_dict(row) for row in rows]
        
        logger.info(f"Retrieved {len(artists)} artists (page {page}, size {page_size}, status: {status or 'all'})")
        logger.info(f"Total artists in database: {total_count}")
        
        return {
            'artists': artists,
            'total': total_count,
            'page': page,
            'page_size': page_size,
            'has_more': offset + len(artists) < total_count
        }

    def update_artist_status(self, artist_id, status):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE artists 
        SET status = ?, last_updated = ?
        WHERE id = ?
        ''', (status, datetime.now().isoformat(), artist_id))
        
        self.conn.commit()
        logger.info(f"Updated artist status: {artist_id} -> {status}")

    def update_artist(self, artist_id: str, artist_data: dict):
        """Update an existing artist's data while preserving their status"""
        try:
            with self.conn.connect() as conn:
                conn.execute(
                    text("""
                        UPDATE artists 
                        SET name = :name,
                            popularity = :popularity,
                            images = :images,
                            last_updated = CURRENT_TIMESTAMP
                        WHERE id = :id
                    """),
                    {
                        'id': artist_id,
                        'name': artist_data['name'],
                        'popularity': artist_data['popularity'],
                        'images': json.dumps(artist_data['images'])
                    }
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Error updating artist {artist_id}: {str(e)}")
            raise

    def _row_to_dict(self, row):
        if not row:
            return None
            
        artist_dict = dict(row)
        
        # Parse images JSON string back to list
        if artist_dict.get('images'):
            artist_dict['images'] = json.loads(artist_dict['images'])
        else:
            artist_dict['images'] = []
            
        return artist_dict

    def __del__(self):
        self.conn.close()
        logger.info("Database connection closed")

    def clear_artists(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM artists')
        self.conn.commit()
        logger.info("Cleared all artists from database") 