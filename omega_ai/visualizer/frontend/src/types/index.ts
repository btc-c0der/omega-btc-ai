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

export interface TrapData {
    id: string;
    type: 'bullish' | 'bearish';
    timestamp: string;
    confidence: number;
    price: number;
    volume: number;
    metadata: Record<string, unknown>;
}

export interface PriceData {
    time: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
}

export interface ChartProps {
    data: {
        prices: PriceData[];
        traps: TrapData[];
    };
}

export interface MetricsData {
    totalTraps: number;
    trapsByType: Record<string, number>;
    averageConfidence: number;
    successRate: number;
    timeDistribution: Record<string, number>;
} 