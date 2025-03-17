import { useState, useEffect, useRef } from 'react';
import { TrapData, PriceData } from '../types';

const WS_BASE_URL = 'ws://localhost:8000';

export interface RealtimeDataFeedResponse<T> {
    data: T | null;
    isConnected: boolean;
    error: Error | null;
}

export function useRealtimeDataFeed<T>(endpoint: string): RealtimeDataFeedResponse<T> {
    const [data, setData] = useState<T | null>(null);
    const [isConnected, setIsConnected] = useState(false);
    const [error, setError] = useState<Error | null>(null);
    const ws = useRef<WebSocket | null>(null);

    useEffect(() => {
        // Create WebSocket connection
        const wsEndpoint = endpoint.startsWith('ws') ? endpoint : `${WS_BASE_URL}${endpoint}`;
        ws.current = new WebSocket(wsEndpoint);

        ws.current.onopen = () => {
            console.log('WebSocket Connected');
            setIsConnected(true);
            setError(null);
        };

        ws.current.onmessage = (event) => {
            try {
                const parsedData = JSON.parse(event.data);
                setData(parsedData);
                setError(null);
            } catch (e) {
                setError(e instanceof Error ? e : new Error('Failed to parse WebSocket data'));
            }
        };

        ws.current.onerror = (event) => {
            console.error('WebSocket error:', event);
            setError(new Error('WebSocket connection error'));
            setIsConnected(false);
        };

        ws.current.onclose = () => {
            console.log('WebSocket Disconnected');
            setIsConnected(false);
        };

        // Cleanup on unmount
        return () => {
            if (ws.current) {
                ws.current.close();
            }
        };
    }, [endpoint]);

    // Implement reconnection logic
    useEffect(() => {
        if (!isConnected && !ws.current) {
            const reconnectTimeout = setTimeout(() => {
                console.log('Attempting to reconnect...');
                ws.current = null; // Reset the WebSocket instance
                // The main useEffect will handle creating a new connection
            }, 5000); // Try to reconnect every 5 seconds

            return () => clearTimeout(reconnectTimeout);
        }
    }, [isConnected]);

    return { data, isConnected, error };
} 