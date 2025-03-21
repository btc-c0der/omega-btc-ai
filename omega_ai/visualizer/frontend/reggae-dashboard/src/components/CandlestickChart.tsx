import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { PositionData } from '../types';
import axios from 'axios';

interface CandlestickChartProps {
    positionData: PositionData | null;
}

interface CandleData {
    timestamp: string[];
    open: number[];
    high: number[];
    low: number[];
    close: number[];
    volume: number[];
}

const CandlestickChart: React.FC<CandlestickChartProps> = ({ positionData }) => {
    const [candleData, setCandleData] = useState<CandleData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Fetch candle data from API
    useEffect(() => {
        const fetchCandleData = async () => {
            try {
                setLoading(true);

                // In production, replace with your API endpoint
                // For now, we'll use a mock API or grab some sample data
                const response = await axios.get('/api/candles');
                setCandleData(response.data);

                setLoading(false);
            } catch (err) {
                console.error('Error fetching candle data:', err);
                setError('Failed to load chart data');
                setLoading(false);

                // Generate mock data for demo purposes
                generateMockData();
            }
        };

        fetchCandleData();

        // Poll for updates
        const interval = setInterval(fetchCandleData, 60000); // Update every minute

        return () => clearInterval(interval);
    }, []);

    // Generate mock data if API fails
    const generateMockData = () => {
        const timestamps = [];
        const opens = [];
        const highs = [];
        const lows = [];
        const closes = [];
        const volumes = [];

        // Current time
        let currentTime = new Date();
        currentTime.setHours(currentTime.getHours() - 24); // Start 24 hours ago

        // Current price around 65000
        let price = 65000;

        // Generate 24 hourly candles
        for (let i = 0; i < 24; i++) {
            // Add timestamp
            timestamps.push(new Date(currentTime).toISOString());

            // Random price movement
            const change = (Math.random() - 0.5) * 1000; // -500 to +500
            const open = price;
            opens.push(open);

            // Update price
            price = open + change;
            closes.push(price);

            // Random high and low
            const highOffset = Math.random() * 500;
            const lowOffset = Math.random() * 500;
            highs.push(Math.max(open, price) + highOffset);
            lows.push(Math.min(open, price) - lowOffset);

            // Random volume
            volumes.push(Math.random() * 1000 + 100);

            // Increment time
            currentTime.setHours(currentTime.getHours() + 1);
        }

        setCandleData({
            timestamp: timestamps,
            open: opens,
            high: highs,
            low: lows,
            close: closes,
            volume: volumes
        });
    };

    if (loading && !candleData) {
        return (
            <div className="bg-reggae-black-light p-4 rounded-lg border border-reggae-gold/20 h-96 flex items-center justify-center">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-reggae-gold"></div>
                    <p className="mt-2 text-reggae-text/70">Loading chart data...</p>
                </div>
            </div>
        );
    }

    if (error && !candleData) {
        return (
            <div className="bg-reggae-black-light p-4 rounded-lg border border-reggae-red/20 h-96 flex items-center justify-center">
                <div className="text-center text-reggae-red">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <p className="mt-2">{error}</p>
                    <p className="mt-1 text-sm">Using demo data instead</p>
                </div>
            </div>
        );
    }

    if (!candleData) {
        return null;
    }

    // Calculate Fibonacci levels if we have a position
    const generateFibLevels = () => {
        if (!positionData || !positionData.has_position || !candleData) {
            return [];
        }

        // Find the min and max prices in our chart
        const minPrice = Math.min(...candleData.low);
        const maxPrice = Math.max(...candleData.high);
        const range = maxPrice - minPrice;

        // Fibonacci levels
        const levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1];

        return levels.map(level => {
            const price = maxPrice - (range * level);
            return {
                type: 'line',
                x0: candleData.timestamp[0],
                x1: candleData.timestamp[candleData.timestamp.length - 1],
                y0: price,
                y1: price,
                line: {
                    color: 'rgba(255, 215, 0, 0.3)',
                    width: 1,
                    dash: 'dot'
                },
                name: `Fib ${level}`
            };
        });
    };

    // Generate position lines
    const generatePositionLines = () => {
        if (!positionData || !positionData.has_position || !candleData) {
            return [];
        }

        const lines = [];

        // Entry line
        if (positionData.entry_price) {
            lines.push({
                type: 'line',
                x0: candleData.timestamp[0],
                x1: candleData.timestamp[candleData.timestamp.length - 1],
                y0: parseFloat(positionData.entry_price.toString()),
                y1: parseFloat(positionData.entry_price.toString()),
                line: {
                    color: 'rgba(255, 221, 0, 0.8)',
                    width: 2
                },
                name: 'Entry'
            });
        }

        // Stop loss line
        if (positionData.stop_loss) {
            lines.push({
                type: 'line',
                x0: candleData.timestamp[0],
                x1: candleData.timestamp[candleData.timestamp.length - 1],
                y0: parseFloat(positionData.stop_loss.toString()),
                y1: parseFloat(positionData.stop_loss.toString()),
                line: {
                    color: 'rgba(255, 61, 0, 0.8)',
                    width: 2
                },
                name: 'Stop Loss'
            });
        }

        // Take profit line
        if (positionData.take_profit) {
            lines.push({
                type: 'line',
                x0: candleData.timestamp[0],
                x1: candleData.timestamp[candleData.timestamp.length - 1],
                y0: parseFloat(positionData.take_profit.toString()),
                y1: parseFloat(positionData.take_profit.toString()),
                line: {
                    color: 'rgba(0, 181, 45, 0.8)',
                    width: 2
                },
                name: 'Take Profit'
            });
        }

        return lines;
    };

    // Plot data
    const plotData = [
        {
            type: 'candlestick',
            x: candleData.timestamp,
            open: candleData.open,
            high: candleData.high,
            low: candleData.low,
            close: candleData.close,
            increasing: { line: { color: '#00B52D' } },
            decreasing: { line: { color: '#FF3D00' } },
            name: 'BTC/USDT'
        },
        {
            type: 'bar',
            x: candleData.timestamp,
            y: candleData.volume,
            marker: {
                color: candleData.close.map((close, i) =>
                    close >= candleData.open[i] ? 'rgba(0, 181, 45, 0.3)' : 'rgba(255, 61, 0, 0.3)'
                )
            },
            name: 'Volume',
            yaxis: 'y2'
        }
    ];

    // Plot layout
    const layout = {
        title: {
            text: 'BTC/USDT',
            font: {
                family: 'Orbitron',
                size: 24,
                color: '#FFD700'
            }
        },
        plot_bgcolor: '#121212',
        paper_bgcolor: '#1E1E1E',
        font: {
            family: 'Fira Code, monospace',
            size: 12,
            color: '#E0E0E0'
        },
        xaxis: {
            gridcolor: 'rgba(255, 215, 0, 0.1)',
            zeroline: false
        },
        yaxis: {
            gridcolor: 'rgba(255, 215, 0, 0.1)',
            zeroline: false,
            side: 'right'
        },
        yaxis2: {
            title: 'Volume',
            overlaying: 'y',
            side: 'left',
            showgrid: false,
            domain: [0, 0.2]
        },
        legend: {
            orientation: 'h',
            y: 1.1,
            bgcolor: 'rgba(30, 30, 30, 0.5)',
            bordercolor: 'rgba(255, 215, 0, 0.3)'
        },
        shapes: [
            ...generateFibLevels(),
            ...generatePositionLines()
        ],
        margin: {
            l: 50,
            r: 50,
            b: 50,
            t: 50,
            pad: 4
        },
        dragmode: 'zoom',
        showlegend: true,
        height: 500
    };

    // Plot config
    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: [
            'sendDataToCloud',
            'autoScale2d',
            'resetScale2d',
            'hoverClosestCartesian',
            'hoverCompareCartesian',
            'lasso2d',
            'select2d'
        ],
        displaylogo: false
    };

    return (
        <div className="bg-reggae-black-light p-4 rounded-lg border border-reggae-gold/20">
            <h2 className="text-xl font-display text-reggae-gold mb-3">OMEGA BTC CHART</h2>
            <div className="chart-container">
                <Plot
                    data={plotData}
                    layout={layout}
                    config={config}
                    style={{ width: '100%', height: '100%' }}
                />
            </div>
            {positionData && positionData.has_position && (
                <div className="text-xs text-center mt-2 text-reggae-text/70">
                    ⚡ <span className="text-reggae-gold">ZION VIBRATION:</span> {' '}
                    {positionData.position_side === 'long' ? 'UPWARD SACRED MOVEMENT' : 'DOWNWARD CORRECTION PATH'}
                </div>
            )}
        </div>
    );
};

export default CandlestickChart; 