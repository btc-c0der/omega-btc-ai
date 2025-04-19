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