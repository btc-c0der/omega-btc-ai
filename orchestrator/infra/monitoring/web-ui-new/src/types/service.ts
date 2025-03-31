export interface ServiceStatus {
    id: string;
    name: string;
    status: 'active' | 'warning' | 'error' | 'inactive';
    uptime: string;
    memoryUsage: number;
    cpuUsage: number;
    lastError?: string;
    lastCheck: string;
    metrics?: ServiceMetrics;
}

export interface ServiceMetrics {
    requestsPerSecond: number;
    responseTime: number;
    errorRate: number;
    connections: number;
}

export interface WebSocketStatus {
    connected: boolean;
    lastMessage?: string;
    lastUpdate: string;
    errors: string[];
} 