import React, { useEffect, useRef } from 'react';

interface WebSocketComponentProps {
    onData: (data: any) => void;
    onConnectionChange: (connected: boolean) => void;
}

const WebSocketComponent: React.FC<WebSocketComponentProps> = ({ onData, onConnectionChange }) => {
    const wsRef = useRef<WebSocket | null>(null);
    const reconnectTimeoutRef = useRef<number | null>(null);

    const connectWebSocket = () => {
        // Get the host from the current URL, fall back to localhost in development
        const host = window.location.hostname === 'localhost'
            ? 'localhost:8000'
            : window.location.host;

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${host}/ws`;

        const ws = new WebSocket(wsUrl);
        wsRef.current = ws;

        ws.onopen = () => {
            console.log('WebSocket connected');
            onConnectionChange(true);

            // Send periodic pings to keep the connection alive
            const pingInterval = setInterval(() => {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send('ping');
                }
            }, 30000); // ping every 30 seconds

            // Store the interval ID in a ref so we can clear it on disconnect
            (ws as any).pingInterval = pingInterval;
        };

        ws.onmessage = (event) => {
            try {
                // Skip "pong" messages
                if (event.data === 'pong') {
                    return;
                }

                // Parse and handle data
                const data = JSON.parse(event.data);
                if (data.type === 'update') {
                    onData(data);
                }
            } catch (e) {
                console.error('Error parsing WebSocket message:', e);
            }
        };

        ws.onclose = () => {
            console.log('WebSocket disconnected');
            onConnectionChange(false);

            // Clear the ping interval
            if ((ws as any).pingInterval) {
                clearInterval((ws as any).pingInterval);
            }

            // Try to reconnect after a delay
            if (reconnectTimeoutRef.current) {
                clearTimeout(reconnectTimeoutRef.current);
            }

            reconnectTimeoutRef.current = window.setTimeout(() => {
                console.log('Attempting to reconnect...');
                connectWebSocket();
            }, 3000);
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            ws.close();
        };
    };

    useEffect(() => {
        // Connect on component mount
        connectWebSocket();

        // Clean up on unmount
        return () => {
            if (wsRef.current) {
                wsRef.current.close();
            }

            if (reconnectTimeoutRef.current) {
                clearTimeout(reconnectTimeoutRef.current);
            }
        };
    }, []);

    // This component doesn't render anything visible
    return null;
};

export default WebSocketComponent; 