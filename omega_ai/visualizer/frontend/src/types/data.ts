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

export interface PriceData {
    time: number;
    open: number;
    close: number;
    high: number;
    low: number;
}

export interface TrapData {
    id: string;
    type: 'bullish' | 'bearish';
    timestamp: number;
    price: number;
    confidence: number;
    volume: number;
    metadata: {
        pattern: string;
        timeframe: string;
    };
}

export interface MetricsData {
    totalTraps: number;
    trapsByType: {
        bullish: number;
        bearish: number;
    };
    averageConfidence: number;
    successRate: number;
    timeDistribution: Record<string, number>;
}

export interface Pattern3DData {
    id: string;
    position: [number, number, number];
    rotation: [number, number, number];
    scale: [number, number, number];
    type: 'bullish' | 'bearish';
    confidence: number;
} 