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

import { TrapData, PriceData, MetricsData } from '../types';

interface TimelineEvent {
    id: string;
    timestamp: string;
    type: string;
    description: string;
}

const API_BASE_URL = 'http://localhost:8000/api';

export async function fetchTraps(): Promise<TrapData[]> {
    try {
        const response = await fetch(`${API_BASE_URL}/traps`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error(`Expected JSON response but got ${contentType}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching traps:', error);
        throw new Error(`Failed to fetch traps: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
}

export async function fetchPriceData(): Promise<PriceData[]> {
    try {
        const response = await fetch(`${API_BASE_URL}/prices`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error(`Expected JSON response but got ${contentType}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching price data:', error);
        throw new Error(`Failed to fetch price data: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
}

export async function fetchMetrics(): Promise<MetricsData> {
    try {
        const response = await fetch(`${API_BASE_URL}/metrics`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error(`Expected JSON response but got ${contentType}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching metrics:', error);
        throw new Error(`Failed to fetch metrics: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
}

export async function fetchTimelineEvents(): Promise<TimelineEvent[]> {
    try {
        const response = await fetch(`${API_BASE_URL}/timeline`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error(`Expected JSON response but got ${contentType}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching timeline events:', error);
        throw new Error(`Failed to fetch timeline events: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
} 