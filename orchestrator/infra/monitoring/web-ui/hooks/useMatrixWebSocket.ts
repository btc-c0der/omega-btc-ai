import { useState, useEffect, useCallback } from 'react';

interface MatrixData {
    testRate: number;
    testFailures: number;
    redisCommands: number;
    marketTrends: number;
    serviceHealth: number;
    testCoverage: number;
}

interface WebSocketState {
    connected: boolean;
    data: MatrixData | null;
}

export const useMatrixWebSocket = (): WebSocketState => {
    const [state, setState] = useState<WebSocketState>({
        connected: false,
        data: null
    });

    const connect = useCallback(() => {
        const ws = new WebSocket('ws://localhost:8080/matrix');

        ws.onopen = () => {
            console.log('Matrix WebSocket connected');
            setState(prev => ({ ...prev, connected: true }));
        };

        ws.onclose = () => {
            console.log('Matrix WebSocket disconnected');
            setState(prev => ({ ...prev, connected: false }));
        };

        ws.onerror = (error) => {
            console.error('Matrix WebSocket error:', error);
            setState(prev => ({ ...prev, connected: false }));
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data) as MatrixData;
                setState(prev => ({ ...prev, data }));
            } catch (error) {
                console.error('Error parsing Matrix data:', error);
            }
        };

        return ws;
    }, []);

    useEffect(() => {
        const ws = connect();

        return () => {
            ws.close();
        };
    }, [connect]);

    return state;
}; 