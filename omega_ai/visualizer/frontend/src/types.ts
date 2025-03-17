export interface PriceData {
    time: string;
    open: number;
    high: number;
    low: number;
    close: number;
}

export interface TrapData {
    id: string;
    type: string;
    timestamp: string;
    confidence: number;
    price: number;
    volume: number;
    metadata: Record<string, any>;
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