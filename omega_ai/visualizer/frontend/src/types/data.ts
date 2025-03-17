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