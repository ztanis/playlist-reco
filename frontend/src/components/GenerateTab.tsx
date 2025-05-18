import React, { useState } from 'react';
import './GenerateTab.css';

const GenerateTab: React.FC = () => {
  const [request, setRequest] = useState('');
  const [tracks, setTracks] = useState<Array<{ name: string; artist: string }>>([]);
  const [playlistName, setPlaylistName] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [trackCount, setTrackCount] = useState(10);
  const [playlistUrl, setPlaylistUrl] = useState<string | null>(null);
  const [considerFavorites, setConsiderFavorites] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setPlaylistUrl(null);
    try {
      const requestData = {
        request,
        track_count: trackCount,
        consider_favorites: considerFavorites
      };

      const response = await fetch('http://localhost:8000/api/playlist/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });
      const data = await response.json();
      console.log('Received data:', data); // Debug log
      
      // Handle nested tracks structure
      if (data.tracks && data.tracks.tracks && Array.isArray(data.tracks.tracks)) {
        setTracks(data.tracks.tracks);
        setPlaylistName(data.tracks.name || 'Generated Playlist');
      } else {
        console.error('Invalid response format:', data);
      }
    } catch (error) {
      console.error('Error generating playlist:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUploadToSpotify = async () => {
    setIsUploading(true);
    try {
      const response = await fetch('http://localhost:8000/api/playlist/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          tracks,
          name: playlistName
        }),
      });
      const data = await response.json();
      setPlaylistUrl(data.playlist_url);
    } catch (error) {
      console.error('Error uploading to Spotify:', error);
    } finally {
      setIsUploading(false);
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
        <label>
          <input
            type="checkbox"
            checked={considerFavorites}
            onChange={(e) => setConsiderFavorites(e.target.checked)}
          />
          Consider favorites
        </label>
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Generating...' : 'Generate Playlist'}
        </button>
      </form>

      {tracks.length > 0 && (
        <div className="tracks-list">
          <div className="tracks-header">
            <div className="playlist-info">
              <h2>{playlistName}</h2>
              <button 
                className="upload-button"
                onClick={handleUploadToSpotify}
                disabled={isUploading}
              >
                {isUploading ? 'Uploading...' : 'Upload to Spotify'}
              </button>
            </div>
          </div>
          {playlistUrl && (
            <div className="playlist-link">
              <a href={playlistUrl} target="_blank" rel="noopener noreferrer">
                Open in Spotify
              </a>
            </div>
          )}
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
