import { useState, useEffect } from 'react';
import { TrapData, PriceData } from '../types';
import { fetchTraps, fetchPriceData, fetchMetrics } from '../services/api';

interface DataFeed {
    traps: TrapData[];
    prices: PriceData[];
    metrics: {
        totalTraps: number;
        trapsByType: Record<string, number>;
        averageConfidence: number;
        successRate: number;
        timeDistribution: Record<string, number>;
    };
    loading: boolean;
    error: string | null;
}

const POLLING_INTERVAL = 30000; // 30 seconds

export const useDataFeed = () => {
    const [data, setData] = useState<DataFeed>({
        traps: [],
        prices: [],
        metrics: {
            totalTraps: 0,
            trapsByType: {},
            averageConfidence: 0,
            successRate: 0,
            timeDistribution: {}
        },
        loading: true,
        error: null
    });

    const fetchData = async () => {
        try {
            const [trapsData, pricesData, metricsData] = await Promise.all([
                fetchTraps(),
                fetchPriceData(),
                fetchMetrics()
            ]);

            setData(prev => ({
                ...prev,
                traps: trapsData,
                prices: pricesData,
                metrics: metricsData,
                loading: false,
                error: null
            }));
        } catch (error) {
            setData(prev => ({
                ...prev,
                loading: false,
                error: error instanceof Error ? error.message : 'Failed to fetch data'
            }));
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, POLLING_INTERVAL);

        return () => {
            clearInterval(interval);
        };
    }, []);

    return data;
};

export default useDataFeed; 