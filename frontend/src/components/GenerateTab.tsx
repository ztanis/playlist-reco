import React, { useState } from 'react';
import './GenerateTab.css';

const GenerateTab: React.FC = () => {
  const [request, setRequest] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [tracks, setTracks] = useState<Array<{ name: string; artist: string; preview_url: string | null }>>([]);

  const handleGenerate = async () => {
    if (!request.trim()) return;

    try {
      setIsGenerating(true);
      const response = await fetch('http://localhost:8000/api/playlist/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ request }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate playlist');
      }

      const data = await response.json();
      setTracks(data.tracks);
    } catch (error) {
      console.error('Error generating playlist:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="generate-tab">
      <div className="generate-form">
        <textarea
          value={request}
          onChange={(e) => setRequest(e.target.value)}
          placeholder="Describe the playlist you want to generate..."
          rows={4}
        />
        <button 
          onClick={handleGenerate}
          disabled={isGenerating || !request.trim()}
        >
          {isGenerating ? 'Generating...' : 'Generate Playlist'}
        </button>
      </div>

      {tracks.length > 0 && (
        <div className="tracks-list">
          <h2>Generated Tracks</h2>
          {tracks.map((track, index) => (
            <div key={index} className="track-item">
              <div className="track-info">
                <span className="track-name">{track.name}</span>
                <span className="track-artist">{track.artist}</span>
              </div>
              {track.preview_url && (
                <audio controls src={track.preview_url}>
                  Your browser does not support the audio element.
                </audio>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GenerateTab;
