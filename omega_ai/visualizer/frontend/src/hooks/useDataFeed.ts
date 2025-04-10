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

import { useState, useEffect, useRef } from 'react';
import { TrapData, PriceData } from '../types';
import { API_BASE_URL } from '../config';

interface WebSocketMessage {
    type: string;
    timestamp: string;
    prices?: any[];
    traps?: any[];
    metrics?: any;
}

export interface DataFeedResponse<T> {
    data: T | null;
    isLoading: boolean;
    error: Error | null;
    isConnected?: boolean;
}

const POLLING_INTERVAL = 30000; // 30 seconds

export function useDataFeed<T>(endpoint: string, initialData: T | null = null, useWebSocket: boolean = false) {
    const [data, setData] = useState<T | null>(initialData);
    const [error, setError] = useState<Error | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isConnected, setIsConnected] = useState(false);
    const wsRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        let isMounted = true;
        let pollInterval: NodeJS.Timeout | null = null;

        const fetchData = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}${endpoint}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const result = await response.json();
                if (isMounted) {
                    setData(result);
                    setError(null);
                }
            } catch (e) {
                if (isMounted) {
                    setError(e as Error);
                }
            } finally {
                if (isMounted) {
                    setIsLoading(false);
                }
            }
        };

        const setupWebSocket = () => {
            const ws = new WebSocket(`ws://localhost:8000/ws`);
            wsRef.current = ws;

            ws.onopen = () => {
                if (isMounted) {
                    setIsConnected(true);
                    setIsLoading(false);
                }
            };

            ws.onmessage = (event) => {
                if (isMounted) {
                    try {
                        const message: WebSocketMessage = JSON.parse(event.data);
                        if (message.type === "initial" || !message.type) {
                            // Extract the relevant data based on the endpoint
                            let relevantData = null;
                            if (endpoint.includes("prices")) {
                                relevantData = message.prices;
                            } else if (endpoint.includes("traps")) {
                                relevantData = message.traps;
                            } else if (endpoint.includes("metrics")) {
                                relevantData = message.metrics;
                            }

                            if (relevantData !== null) {
                                setData(relevantData as T);
                            }
                        }
                    } catch (e) {
                        console.error("WebSocket message parsing error:", e);
                    }
                }
            };

            ws.onerror = (event) => {
                if (isMounted) {
                    setError(new Error("WebSocket error"));
                    setIsConnected(false);
                }
            };

            ws.onclose = () => {
                if (isMounted) {
                    setIsConnected(false);
                    // Attempt to reconnect after 5 seconds
                    setTimeout(() => {
                        if (isMounted && useWebSocket) {
                            setupWebSocket();
                        }
                    }, 5000);
                }
            };
        };

        if (useWebSocket) {
            setupWebSocket();
        } else {
            fetchData();
            // Poll every 30 seconds for non-WebSocket connections
            pollInterval = setInterval(fetchData, POLLING_INTERVAL);
        }

        return () => {
            isMounted = false;
            if (pollInterval) {
                clearInterval(pollInterval);
            }
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, [endpoint, useWebSocket]);

    return {
        data,
        error,
        isLoading,
        isConnected: useWebSocket ? isConnected : undefined
    };
}

export default useDataFeed; 