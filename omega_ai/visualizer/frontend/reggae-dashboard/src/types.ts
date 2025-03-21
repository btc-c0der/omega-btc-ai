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
    jah_message?: string;
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