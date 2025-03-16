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