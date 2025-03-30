import { useEffect, useState } from 'react';
import { fetchFearGreedIndex, FearGreedData } from '../../services/fearGreedService';

const FearGreedWidget = () => {
    const [fearGreedData, setFearGreedData] = useState<FearGreedData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const getFearGreedData = async () => {
            try {
                setLoading(true);
                const data = await fetchFearGreedIndex();
                setFearGreedData(data);
                setError(null);
            } catch (err) {
                setError('Failed to fetch Fear & Greed Index');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        getFearGreedData();

        // Refresh data every 30 minutes
        const intervalId = setInterval(getFearGreedData, 30 * 60 * 1000);

        return () => clearInterval(intervalId);
    }, []);

    const getColorByValue = (value: number): string => {
        if (value <= 25) return '#F44336'; // Extreme Fear - Red
        if (value <= 40) return '#FF9800'; // Fear - Orange
        if (value <= 60) return '#FFC107'; // Neutral - Yellow
        if (value <= 80) return '#4CAF50'; // Greed - Green
        return '#8BC34A'; // Extreme Greed - Light Green
    };

    const getGaugeRotation = (value: number): number => {
        // Convert value (0-100) to rotation (-90 to 90 degrees)
        return (value / 100) * 180 - 90;
    };

    if (loading) {
        return (
            <div className="bg-gray-800 p-4 rounded-lg shadow-lg animate-pulse">
                <h2 className="text-lg font-semibold text-gray-200 mb-2">
                    Fear & Greed Index
                </h2>
                <div className="h-32 bg-gray-700 rounded flex items-center justify-center">
                    <div className="text-gray-500">Loading...</div>
                </div>
            </div>
        );
    }

    if (error || !fearGreedData) {
        return (
            <div className="bg-gray-800 p-4 rounded-lg shadow-lg">
                <h2 className="text-lg font-semibold text-gray-200 mb-2">
                    Fear & Greed Index
                </h2>
                <div className="text-red-400 text-center p-4">
                    {error || 'Unable to load data'}
                </div>
            </div>
        );
    }

    const rotation = getGaugeRotation(fearGreedData.value);
    const color = getColorByValue(fearGreedData.value);
    const timestamp = new Date(fearGreedData.timestamp).toLocaleString();

    return (
        <div className="bg-gray-800 p-4 rounded-lg shadow-lg">
            <h2 className="text-lg font-semibold text-gray-200 mb-2">
                Crypto Fear & Greed Index
            </h2>

            <div className="flex flex-col items-center mb-4">
                <div className="text-4xl font-bold" style={{ color }}>
                    {fearGreedData.value}
                </div>
                <div
                    className="text-lg font-medium mt-1"
                    style={{ color }}
                >
                    {fearGreedData.valueClassification}
                </div>
            </div>

            {/* Gauge visualization */}
            <div className="relative h-20 w-full mb-3">
                {/* Gauge background */}
                <div className="absolute inset-0 flex items-center justify-center">
                    <div className="h-16 w-full bg-gray-700 rounded-full overflow-hidden">
                        <div className="flex h-full">
                            <div className="w-1/5 h-full bg-red-500" title="Extreme Fear"></div>
                            <div className="w-1/5 h-full bg-orange-500" title="Fear"></div>
                            <div className="w-1/5 h-full bg-yellow-500" title="Neutral"></div>
                            <div className="w-1/5 h-full bg-green-500" title="Greed"></div>
                            <div className="w-1/5 h-full bg-lime-500" title="Extreme Greed"></div>
                        </div>
                    </div>
                </div>

                {/* Pointer */}
                <div className="absolute inset-0 flex items-center justify-center">
                    <div
                        className="h-14 w-1 bg-white origin-bottom transform"
                        style={{
                            transform: `rotate(${rotation}deg)`,
                            transformOrigin: 'bottom center',
                            marginBottom: '2px'
                        }}
                    >
                        <div className="h-2 w-2 rounded-full bg-white -mt-1 -ml-0.5"></div>
                    </div>
                </div>
            </div>

            <div className="text-xs text-gray-400 text-right">
                Last updated: {timestamp}
            </div>
            <div className="text-xs text-gray-400 text-right">
                Next update in: {fearGreedData.timeUntilUpdate}
            </div>
            <div className="text-xs text-gray-400 text-right mt-1">
                <a
                    href="https://alternative.me/crypto/fear-and-greed-index/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:underline"
                >
                    Data source: Fear & Greed Index
                </a>
            </div>
        </div>
    );
};

export default FearGreedWidget; 