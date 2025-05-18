import React, { useState, useEffect } from 'react';
import './App.css';
import ArtistList from './components/ArtistList';
import TabBar from './components/TabBar';
import GenerateTab from './components/GenerateTab';

interface Artist {
  id: string;
  name: string;
  popularity: number;
  status: string;
  images: Array<{ url: string }>;
}

interface ArtistsResponse {
  artists: Artist[];
}

function App() {
  const [artists, setArtists] = useState<Artist[]>([]);
  const [activeTab, setActiveTab] = useState('artists');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchArtists();
  }, []);

  const fetchArtists = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/artists');
      if (!response.ok) {
        throw new Error('Failed to fetch artists');
      }
      const data: ArtistsResponse = await response.json();
      setArtists(data.artists);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (artistId: string, status: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/artists/${artistId}/status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status }),
      });

      if (response.ok) {
        fetchArtists(); // Refresh the list
      }
    } catch (error) {
      setError('Failed to update artist status');
      console.error('Error updating status:', error);
    }
  };

  const handleSync = async () => {
    setLoading(true);
    setError(null);
    try {
      // Get auth URL
      const authResponse = await fetch('http://localhost:8000/api/spotify/auth-url');
      const { auth_url } = await authResponse.json();
      
      // Open Spotify auth in a popup
      const width = 600;
      const height = 700;
      const left = window.screenX + (window.outerWidth - width) / 2;
      const top = window.screenY + (window.outerHeight - height) / 2;
      
      const popup = window.open(
        auth_url,
        'Spotify Auth',
        `width=${width},height=${height},left=${left},top=${top}`
      );

      // Listen for the callback
      window.addEventListener('message', async (event) => {
        if (event.data.type === 'spotify-auth-callback') {
          const code = event.data.code;
          popup?.close();

          // Call sync endpoint
          const syncResponse = await fetch('http://localhost:8000/api/spotify/sync', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code }),
          });

          if (!syncResponse.ok) {
            throw new Error('Failed to sync artists');
          }

          await fetchArtists();
          setLoading(false);
        }
      });
    } catch (err) {
      setError('Failed to sync artists');
      console.error(err);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading artists...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="app">
      <TabBar activeTab={activeTab} onTabChange={setActiveTab} />
      <div className="content">
        {activeTab === 'artists' ? (
          <ArtistList artists={artists} onStatusChange={handleStatusChange} />
        ) : (
          <GenerateTab />
        )}
      </div>
    </div>
  );
}

export default App;
