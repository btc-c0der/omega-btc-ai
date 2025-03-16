export interface PriceData {
    time: string;
    open: number;
    high: number;
    low: number;
    close: number;
}

export interface TrapData {
    id: string;
    type: 'bullish' | 'bearish';
    timestamp: string;
    confidence: number;
    price: number;
    volume: number;
    metadata: Record<string, unknown>;
}

export interface ChartData {
    prices: PriceData[];
    traps: TrapData[];
}

export interface ChartProps {
    data: ChartData;
}

export interface MetricsData {
    totalTraps: number;
    trapsByType: Record<string, number>;
    averageConfidence: number;
    successRate: number;
    timeDistribution: Record<string, number>;
} 