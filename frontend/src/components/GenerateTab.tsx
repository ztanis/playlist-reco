import React, { useState } from 'react';
import './GenerateTab.css';

const GenerateTab: React.FC = () => {
  const [request, setRequest] = useState('');
  const [tracks, setTracks] = useState<Array<{ name: string; artist: string }>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [trackCount, setTrackCount] = useState(10);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/playlist/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ request, track_count: trackCount }),
      });
      const data = await response.json();
      setTracks(data.tracks);
    } catch (error) {
      console.error('Error generating playlist:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="generate-tab">
      <form onSubmit={handleSubmit} className="generate-form">
        <textarea
          value={request}
          onChange={(e) => setRequest(e.target.value)}
          placeholder="Describe the playlist you want to generate..."
          required
        />
        <div className="track-count-selector">
          <label>Number of tracks:</label>
          <select 
            value={trackCount} 
            onChange={(e) => setTrackCount(Number(e.target.value))}
          >
            <option value={10}>10 tracks</option>
            <option value={20}>20 tracks</option>
            <option value={30}>30 tracks</option>
            <option value={40}>40 tracks</option>
            <option value={50}>50 tracks</option>
          </select>
        </div>
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Generating...' : 'Generate Playlist'}
        </button>
      </form>

      {tracks.length > 0 && (
        <div className="tracks-list">
          <h2>Generated Playlist</h2>
          {tracks.map((track, index) => (
            <div key={index} className="track-item">
              <div className="track-info">
                <span className="track-name">{track.name}</span>
                <span className="track-artist">{track.artist}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GenerateTab;
