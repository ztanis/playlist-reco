import React from 'react';
import './TabBar.css';

interface TabBarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const TabBar: React.FC<TabBarProps> = ({ activeTab, onTabChange }) => {
  return (
    <div className="tab-bar">
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
  );
};

export default TabBar; 