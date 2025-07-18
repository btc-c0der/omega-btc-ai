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

import { useState, useCallback } from 'react';
import { useWebSocket } from './useWebSocket';
import { PriceData } from '../types';

const WS_URL = 'ws://localhost:8766';
const MAX_HISTORY = 100;

export const useRealtimePriceData = () => {
    const [priceHistory, setPriceHistory] = useState<PriceData[]>([]);

    const onMessage = useCallback((data: any) => {
        if (data.btc_price) {
            const timestamp = new Date();
            const newPrice: PriceData = {
                time: timestamp.toISOString(),
                open: data.btc_price,
                close: data.btc_price,
                high: data.btc_price,
                low: data.btc_price,
                volume: data.volume || 0
            };

            setPriceHistory(prev => {
                const updated = [...prev, newPrice].slice(-MAX_HISTORY);

                // Update previous candle if it's within the same minute
                if (updated.length > 1) {
                    const lastCandle = updated[updated.length - 2];
                    const lastTime = new Date(lastCandle.time);
                    if (timestamp.getMinutes() === lastTime.getMinutes()) {
                        lastCandle.close = data.btc_price;
                        lastCandle.high = Math.max(lastCandle.high, data.btc_price);
                        lastCandle.low = Math.min(lastCandle.low, data.btc_price);
                        if (data.volume) {
                            lastCandle.volume += data.volume;
                        }
                        return [...updated.slice(0, -1)];
                    }
                }

                return updated;
            });
        }
    }, []);

    const { isConnected, error } = useWebSocket(WS_URL, {
        onMessage,
        reconnectAttempts: Infinity,
        reconnectInterval: 2000
    });

    return {
        data: priceHistory,
        isConnected,
        error
    };
}; 