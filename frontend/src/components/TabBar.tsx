import React from 'react';
import './TabBar.css';

interface TabBarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const TabBar: React.FC<TabBarProps> = ({ activeTab, onTabChange }) => {
  const handleSpotifyLogin = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/spotify/auth-url');
      const data = await response.json();
      
      // Open Spotify auth in a new window
      const width = 600;
      const height = 700;
      const left = window.screenX + (window.outerWidth - width) / 2;
      const top = window.screenY + (window.outerHeight - height) / 2;
      window.open(
        data.auth_url,
        'Spotify Auth',
        `width=${width},height=${height},left=${left},top=${top}`
      );
    } catch (error) {
      console.error('Error getting Spotify auth URL:', error);
    }
  };

  return (
    <div className="tab-bar">
      <div className="tab-group">
        <button
          className={`tab ${activeTab === 'artists' ? 'active' : ''}`}
          onClick={() => onTabChange('artists')}
        >
          Artists
        </button>
        <button
          className={`tab ${activeTab === 'generate' ? 'active' : ''}`}
          onClick={() => onTabChange('generate')}
        >
          Generate Playlist
        </button>
      </div>
      <button
        className="spotify-login-button"
        onClick={handleSpotifyLogin}
      >
        Login to Spotify
      </button>
    </div>
  );
};

export default TabBar; 