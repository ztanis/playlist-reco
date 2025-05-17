export interface Artist {
    id: string;
    name: string;
    popularity: number;
    status: string;
    images: Array<{
        url: string;
        height: number;
        width: number;
    }>;
}

export type ArtistStatus = 'not_ranked' | 'like' | 'dislike' | 'neutral'; 