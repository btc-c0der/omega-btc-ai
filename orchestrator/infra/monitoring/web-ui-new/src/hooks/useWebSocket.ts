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