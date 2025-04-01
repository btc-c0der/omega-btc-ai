import { useEffect, useState, useRef } from 'react';
import { fetchFearGreedHistory } from '../../services/fearGreedService';
import * as d3 from 'd3';

interface ChartData {
    date: Date;
    value: number;
    classification: string;
}

const FearGreedChart = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [data, setData] = useState<ChartData[]>([]);

    const svgRef = useRef<SVGSVGElement>(null);
    const chartRef = useRef<HTMLDivElement>(null);

    // Fetch data
    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const result = await fetchFearGreedHistory(30);

                // Transform API data to chart format
                const chartData = result.data.map(item => ({
                    date: new Date(item.timestamp),
                    value: item.value,
                    classification: item.valueClassification
                })).sort((a, b) => a.date.getTime() - b.date.getTime());

                setData(chartData);
                setError(null);
            } catch (err) {
                console.error('Error fetching fear greed history:', err);
                setError('Failed to load Fear & Greed history');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    // Draw chart when data changes
    useEffect(() => {
        if (!data.length || !svgRef.current || !chartRef.current) return;

        // Clear previous chart
        d3.select(svgRef.current).selectAll('*').remove();

        // Get parent dimensions
        const containerWidth = chartRef.current.clientWidth;
        const margin = { top: 20, right: 20, bottom: 30, left: 40 };
        const width = containerWidth - margin.left - margin.right;
        const height = 200 - margin.top - margin.bottom;

        // Create SVG
        const svg = d3.select(svgRef.current)
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        // Create scales
        const x = d3.scaleTime()
            .domain(d3.extent(data, d => d.date) as [Date, Date])
            .range([0, width]);

        const y = d3.scaleLinear()
            .domain([0, 100])
            .range([height, 0]);

        // Add X axis
        svg.append('g')
            .attr('transform', `translate(0,${height})`)
            .style('color', '#9ca3af') // gray-400
            .call(d3.axisBottom(x).ticks(5).tickFormat(d => {
                const date = new Date(d as Date);
                return `${date.getMonth() + 1}/${date.getDate()}`;
            }));

        // Add Y axis
        svg.append('g')
            .style('color', '#9ca3af') // gray-400
            .call(d3.axisLeft(y).ticks(5));

        // Add background zones
        const zones = [
            { min: 0, max: 25, label: 'Extreme Fear', color: 'rgba(244, 67, 54, 0.1)' },
            { min: 25, max: 40, label: 'Fear', color: 'rgba(255, 152, 0, 0.1)' },
            { min: 40, max: 60, label: 'Neutral', color: 'rgba(255, 193, 7, 0.1)' },
            { min: 60, max: 80, label: 'Greed', color: 'rgba(76, 175, 80, 0.1)' },
            { min: 80, max: 100, label: 'Extreme Greed', color: 'rgba(139, 195, 74, 0.1)' }
        ];

        zones.forEach(zone => {
            svg.append('rect')
                .attr('x', 0)
                .attr('y', y(zone.max))
                .attr('width', width)
                .attr('height', y(zone.min) - y(zone.max))
                .attr('fill', zone.color);

            // Zone labels
            svg.append('text')
                .attr('x', width - 5)
                .attr('y', y((zone.min + zone.max) / 2))
                .attr('dy', '0.35em')
                .attr('text-anchor', 'end')
                .attr('fill', '#9ca3af')
                .style('font-size', '9px')
                .text(zone.label);
        });

        // Add line
        const line = d3.line<ChartData>()
            .x(d => x(d.date))
            .y(d => y(d.value))
            .curve(d3.curveMonotoneX);

        svg.append('path')
            .datum(data)
            .attr('fill', 'none')
            .attr('stroke', '#3b82f6') // blue-500
            .attr('stroke-width', 2)
            .attr('d', line);

        // Add dots
        svg.selectAll('.dot')
            .data(data)
            .enter().append('circle')
            .attr('class', 'dot')
            .attr('cx', d => x(d.date))
            .attr('cy', d => y(d.value))
            .attr('r', 3)
            .attr('fill', d => {
                if (d.value <= 25) return '#F44336'; // Extreme Fear
                if (d.value <= 40) return '#FF9800'; // Fear
                if (d.value <= 60) return '#FFC107'; // Neutral
                if (d.value <= 80) return '#4CAF50'; // Greed
                return '#8BC34A'; // Extreme Greed
            });

        // Add grid lines
        svg.append('g')
            .attr('class', 'grid')
            .style('stroke-dasharray', '3,3')
            .style('opacity', 0.2)
            .call(
                d3.axisLeft(y)
                    .tickSize(-width)
                    .tickFormat(() => '')
                    .ticks(5)
            );

    }, [data]);

    if (loading) {
        return (
            <div className="bg-gray-800 p-4 rounded-lg shadow-lg h-64 animate-pulse">
                <h2 className="text-lg font-semibold text-gray-200 mb-2">
                    Fear & Greed Index History
                </h2>
                <div className="h-full flex items-center justify-center">
                    <div className="text-gray-500">Loading chart data...</div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-gray-800 p-4 rounded-lg shadow-lg h-64">
                <h2 className="text-lg font-semibold text-gray-200 mb-2">
                    Fear & Greed Index History
                </h2>
                <div className="text-red-400 text-center h-full flex items-center justify-center">
                    {error}
                </div>
            </div>
        );
    }

    return (
        <div className="bg-gray-800 p-4 rounded-lg shadow-lg">
            <h2 className="text-lg font-semibold text-gray-200 mb-2">
                30-Day Fear & Greed Index History
            </h2>
            <div ref={chartRef} className="w-full h-52">
                <svg ref={svgRef}></svg>
            </div>
            <div className="text-xs text-gray-400 text-center mt-2">
                Historical data from the Crypto Fear & Greed Index
            </div>
        </div>
    );
};

export default FearGreedChart; 