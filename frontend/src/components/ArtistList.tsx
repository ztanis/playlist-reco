import React, { useState } from 'react';
import './ArtistList.css';

interface Artist {
  id: string;
  name: string;
  popularity: number;
  status: string;
  images: Array<{ url: string }>;
}

interface ArtistListProps {
  artists: Artist[];
  onStatusChange: (artistId: string, status: string) => void;
}

const statusOptions = [
  { value: 'not_ranked', label: 'Not Ranked', icon: '❓' },
  { value: 'like', label: 'Like', icon: '👍' },
  { value: 'dislike', label: 'Dislike', icon: '👎' },
  { value: 'neutral', label: 'Neutral', icon: '➖' },
];

const ArtistList: React.FC<ArtistListProps> = ({ artists, onStatusChange }) => {
  const [selectedStatus, setSelectedStatus] = useState('');

  const filteredArtists = selectedStatus
    ? artists.filter(artist => artist.status === selectedStatus)
    : artists;

  return (
    <div className="artist-list">
      <div className="status-filter">
        <div className="filter-controls">
          <label htmlFor="status-select">Filter by status:</label>
          <select
            id="status-select"
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
          >
            <option value="">All</option>
            {statusOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div className="artist-count">
          {filteredArtists.length} artists
        </div>
      </div>

      <div className="artists-grid">
        {filteredArtists.map(artist => (
          <div key={artist.id} className="artist-card">
            <img
              src={artist.images[0]?.url || '/default-artist.png'}
              alt={artist.name}
              className="artist-image"
            />
            <h3 className="artist-name">{artist.name}</h3>
            <div className="artist-popularity">
              Popularity: {artist.popularity}
            </div>
            <div className="artist-status-buttons">
              {statusOptions.map(option => (
                <button
                  key={option.value}
                  className={`status-btn ${option.value} ${artist.status === option.value ? 'active' : ''}`}
                  onClick={() => onStatusChange(artist.id, option.value)}
                  title={option.label}
                  type="button"
                >
                  <span role="img" aria-label={option.label}>{option.icon}</span>
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ArtistList; 