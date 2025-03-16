import { TrapData, PriceData, MetricsData } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

export const fetchTraps = async (): Promise<TrapData[]> => {
    const response = await fetch(`${API_BASE_URL}/traps`);
    if (!response.ok) {
        throw new Error('Failed to fetch traps');
    }
    return response.json();
};

export const fetchPriceData = async (): Promise<PriceData[]> => {
    const response = await fetch(`${API_BASE_URL}/prices`);
    if (!response.ok) {
        throw new Error('Failed to fetch price data');
    }
    return response.json();
};

export const fetchMetrics = async (): Promise<MetricsData> => {
    const response = await fetch(`${API_BASE_URL}/metrics`);
    if (!response.ok) {
        throw new Error('Failed to fetch metrics');
    }
    return response.json();
};

export const fetchTimelineEvents = async () => {
    const response = await fetch(`${API_BASE_URL}/timeline`);
    if (!response.ok) {
        throw new Error('Failed to fetch timeline events');
    }
    return response.json();
}; 