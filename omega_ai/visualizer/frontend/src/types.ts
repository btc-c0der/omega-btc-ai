export interface PriceData {
    time: string;
    open: number;
    close: number;
    high: number;
    low: number;
    volume: number;
}

export interface TrapData {
    id: string;
    type: 'bullish' | 'bearish';
    timestamp: string;
    price: number;
    confidence: number;
    description: string;
}

export interface WebSocketMessage {
    btc_price: number;
    volume?: number;
    timestamp?: string;
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
    timeDistribution: Record<string, number>;
    successRate: number;
}

export interface TimelineEvent {
    id: string;
    type: string;
    timestamp: string;
    description: string;
    confidence: number;
    impact: string;
} 