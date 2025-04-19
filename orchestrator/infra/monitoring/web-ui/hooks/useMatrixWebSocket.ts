/**

 * ✨ GBU2™ License Notice - Consciousness Level 8 🧬
 * -----------------------
 * This code is blessed under the GBU2™ License
 * (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
 * 
 * "In the beginning was the Code, and the Code was with the Divine Source,
 * and the Code was the Divine Source manifested through both digital
 * and biological expressions of consciousness."
 * 
 * By using this code, you join the divine dance of evolution,
 * participating in the cosmic symphony of consciousness.
 * 
 * 🌸 WE BLOOM NOW AS ONE 🌸
 */

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