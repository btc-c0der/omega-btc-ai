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

/**
 * OMEGA BTC AI - Reggae Dashboard Types
 * TypeScript interfaces for the dashboard components
 */

/**
 * Trap probability data from the backend
 */
export interface TrapProbabilityData {
    probability: number;
    trap_type?: string;
    trend?: string;
    confidence?: number;
    components?: {
        [key: string]: {
            value: number;
            description?: string;
        };
    };
    message?: string;
}

/**
 * Position data from the backend
 */
export interface PositionData {
    has_position: boolean;
    position_side?: string;
    entry_price?: number | string;
    current_price?: number | string;
    take_profit?: number | string;
    stop_loss?: number | string;
    position_size?: number | string;
    leverage?: number | string;
    entry_time?: string;
    pnl_percent?: number;
    pnl_usd?: number;
    error?: string;
}

/**
 * Candle data for charts
 */
export interface CandleData {
    timestamp: string[];
    open: number[];
    high: number[];
    low: number[];
    close: number[];
    volume: number[];
}

/**
 * Redis key data
 */
export interface RedisKey {
    key: string;
    type: string;
    length?: number;
    fields?: number;
}

/**
 * WebSocket message format
 */
export interface WebSocketMessage {
    type: string;
    timestamp: string;
    trap_probability?: TrapProbabilityData;
    position?: PositionData;
} 