import { useState, useEffect } from 'react';
import { WebSocketStatus } from '../types/service';

export const useWebSocket = (endpoint: string): boolean => {
    const [status, setStatus] = useState<WebSocketStatus>({
        connected: false,
        lastUpdate: new Date().toISOString(),
        errors: []
    });

    useEffect(() => {
        const ws = new WebSocket(endpoint);

        ws.onopen = () => {
            setStatus(prev => ({
                ...prev,
                connected: true,
                lastUpdate: new Date().toISOString()
            }));
        };

        ws.onclose = () => {
            setStatus(prev => ({
                ...prev,
                connected: false,
                lastUpdate: new Date().toISOString()
            }));
        };

        ws.onerror = (error) => {
            setStatus(prev => ({
                ...prev,
                errors: [...prev.errors, error.toString()],
                lastUpdate: new Date().toISOString()
            }));
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                setStatus(prev => ({
                    ...prev,
                    lastMessage: data,
                    lastUpdate: new Date().toISOString()
                }));
            } catch (error) {
                setStatus(prev => ({
                    ...prev,
                    errors: [...prev.errors, 'Failed to parse message'],
                    lastUpdate: new Date().toISOString()
                }));
            }
        };

        return () => {
            ws.close();
        };
    }, [endpoint]);

    return status.connected;
}; 