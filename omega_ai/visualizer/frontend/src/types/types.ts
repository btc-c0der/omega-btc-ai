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
    type: 'FAKE_PUMP' | 'FAKE_DUMP' | 'LIQUIDITY_GRAB' | 'HALF_LIQUIDITY_GRAB';
    timestamp: string;
    confidence: number;
    price?: number;
    volume?: number;
    metadata?: Record<string, any>;
}

export interface PriceData {
    timestamp: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
}

export interface MetricsData {
    totalTraps: number;
    trapsByType: Record<string, number>;
    averageConfidence: number;
    timeDistribution: Record<string, number>;
    successRate: number;
}

export interface TimelineEvent {
    id: string;
    type: TrapData['type'];
    timestamp: string;
    description: string;
    confidence: number;
    impact: 'HIGH' | 'MEDIUM' | 'LOW';
}

export interface HeatMapData {
    timestamp: string;
    price: number;
    intensity: number;
    type: TrapData['type'];
}

export interface Pattern3DData {
    x: number; // Price
    y: number; // Volume
    z: number; // Time
    type: TrapData['type'];
    confidence: number;
} 