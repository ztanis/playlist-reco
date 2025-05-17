import React, { useState } from 'react';
import './PlaylistGenerator.css';

interface Track {
  name: string;
  artist: string;
  preview_url: string | null;
}

interface PlaylistGeneratorProps {
  onGenerate: (request: string) => Promise<void>;
  isLoading: boolean;
  tracks: Track[];
}

const PlaylistGenerator: React.FC<PlaylistGeneratorProps> = ({ onGenerate, isLoading, tracks }) => {
  const [request, setRequest] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (request.trim()) {
      await onGenerate(request);
    }
  };

  return (
    <div className="playlist-generator">
      <form onSubmit={handleSubmit} className="generator-form">
        <div className="form-group">
          <label htmlFor="playlist-request">Describe your playlist:</label>
          <textarea
            id="playlist-request"
            value={request}
            onChange={(e) => setRequest(e.target.value)}
            placeholder="e.g., 'A playlist for a rainy day with indie and folk songs'"
            rows={4}
            required
          />
        </div>
        <button 
          type="submit" 
          className="generate-button"
          disabled={isLoading}
        >
          {isLoading ? 'Generating...' : 'Generate Playlist'}
        </button>
      </form>

      {tracks.length > 0 && (
        <div className="tracks-list">
          <h2>Generated Tracks</h2>
          <div className="tracks-grid">
            {tracks.map((track, index) => (
              <div key={index} className="track-card">
                <h3>{track.name}</h3>
                <p className="artist-name">{track.artist}</p>
                {track.preview_url && (
                  <audio controls className="track-preview">
                    <source src={track.preview_url} type="audio/mpeg" />
                    Your browser does not support the audio element.
                  </audio>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PlaylistGenerator; 