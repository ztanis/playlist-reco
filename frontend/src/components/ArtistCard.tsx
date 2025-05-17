import React from 'react';
import { Artist, ArtistStatus } from '../types';
import { updateArtistStatus } from '../api';
import './ArtistCard.css';

interface ArtistCardProps {
    artist: Artist;
    onStatusUpdate: (artistId: string, status: ArtistStatus) => void;
}

const ArtistCard: React.FC<ArtistCardProps> = ({ artist, onStatusUpdate }) => {
    const handleStatusClick = async (status: ArtistStatus) => {
        try {
            await updateArtistStatus(artist.id, status);
            onStatusUpdate(artist.id, status);
        } catch (error) {
            console.error('Failed to update status:', error);
        }
    };

    return (
        <div className="artist-card" id={`artist-${artist.id}`}>
            <img
                src={artist.images[0]?.url || 'https://via.placeholder.com/80'}
                className="artist-image"
                alt={artist.name}
            />
            <div className="artist-info">
                <div className="artist-name">{artist.name}</div>
                <div className="artist-popularity">Popularity: {artist.popularity}%</div>
                <div className="ranking-buttons">
                    <button
                        type="button"
                        className={`ranking-button not-ranked ${artist.status === 'not_ranked' ? 'active' : ''}`}
                        onClick={() => handleStatusClick('not_ranked')}
                    >
                        ⭐ Not Ranked
                    </button>
                    <button
                        type="button"
                        className={`ranking-button like ${artist.status === 'like' ? 'active' : ''}`}
                        onClick={() => handleStatusClick('like')}
                    >
                        ❤️ Like
                    </button>
                    <button
                        type="button"
                        className={`ranking-button dislike ${artist.status === 'dislike' ? 'active' : ''}`}
                        onClick={() => handleStatusClick('dislike')}
                    >
                        👎 Dislike
                    </button>
                    <button
                        type="button"
                        className={`ranking-button neutral ${artist.status === 'neutral' ? 'active' : ''}`}
                        onClick={() => handleStatusClick('neutral')}
                    >
                        ➖ Neutral
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ArtistCard; 