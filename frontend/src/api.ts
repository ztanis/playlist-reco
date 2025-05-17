import { Artist, ArtistStatus } from './types';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

export const getArtists = async (status?: string): Promise<Artist[]> => {
    const url = status ? `${API_BASE_URL}/artists?status=${status}` : `${API_BASE_URL}/artists`;
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error('Failed to fetch artists');
    }
    const data = await response.json();
    return data.artists;
};

export const updateArtistStatus = async (artistId: string, status: ArtistStatus): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/artists/${artistId}/status`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status }),
    });
    if (!response.ok) {
        throw new Error('Failed to update artist status');
    }
}; 