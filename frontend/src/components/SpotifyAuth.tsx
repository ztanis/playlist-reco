import React, { useEffect, useState } from 'react';
import './SpotifyAuth.css';

const SpotifyAuth: React.FC = () => {
    const [authUrl, setAuthUrl] = useState<string>('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchAuthUrl = async () => {
            try {
                const response = await fetch('/api/spotify/auth-url');
                if (!response.ok) {
                    throw new Error('Failed to get auth URL');
                }
                const data = await response.json();
                setAuthUrl(data.auth_url);
            } catch (err) {
                setError('Failed to initialize Spotify authentication');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchAuthUrl();
    }, []);

    const handleCallback = async () => {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');

        if (code) {
            try {
                setLoading(true);
                const response = await fetch(`/api/spotify/callback?code=${code}`);
                if (!response.ok) {
                    throw new Error('Failed to load artists');
                }
                // Remove the code from URL
                window.history.replaceState({}, document.title, window.location.pathname);
                // Reload the page to show the loaded artists
                window.location.reload();
            } catch (err) {
                setError('Failed to load artists from Spotify');
                console.error(err);
            } finally {
                setLoading(false);
            }
        }
    };

    useEffect(() => {
        handleCallback();
    }, []);

    if (loading) {
        return <div className="spotify-auth-loading">Loading...</div>;
    }

    if (error) {
        return <div className="spotify-auth-error">{error}</div>;
    }

    return (
        <div className="spotify-auth">
            <h2>Connect with Spotify</h2>
            <p>Load your top artists from Spotify to start ranking them.</p>
            <a href={authUrl} className="spotify-auth-button">
                Connect to Spotify
            </a>
        </div>
    );
};

export default SpotifyAuth; 