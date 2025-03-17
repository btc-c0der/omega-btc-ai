import { useState, useEffect } from 'react';
import { TrapData, PriceData } from '../types';

const API_BASE_URL = 'http://localhost:8000';

export interface DataFeedResponse<T> {
    data: T | null;
    isLoading: boolean;
    error: Error | null;
}

const POLLING_INTERVAL = 30000; // 30 seconds

export function useDataFeed<T>(endpoint: string): DataFeedResponse<T> {
    const [data, setData] = useState<T | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Use the full URL
                const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const contentType = response.headers.get("content-type");
                if (!contentType || !contentType.includes("application/json")) {
                    throw new Error(`Expected JSON response but got ${contentType}`);
                }
                const result = await response.json();
                setData(result);
                setError(null);
            } catch (e) {
                setError(e instanceof Error ? e : new Error('Unknown error occurred'));
                setData(null);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();

        // Set up polling
        const intervalId = setInterval(fetchData, POLLING_INTERVAL);

        // Cleanup on unmount
        return () => clearInterval(intervalId);
    }, [endpoint]);

    return { data, isLoading, error };
}

export default useDataFeed; 