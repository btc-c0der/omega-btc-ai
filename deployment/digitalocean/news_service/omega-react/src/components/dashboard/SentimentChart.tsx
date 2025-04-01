import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

const SentimentChart = () => {
    const chartRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!chartRef.current) return;

        // In a real app, we would render a chart with D3 or another library
        // For now, we'll just show a placeholder
        const renderPlaceholderChart = () => {
            const container = chartRef.current;
            if (!container) return;

            // Create a simple placeholder chart with HTML/CSS
            container.innerHTML = '';
            const chartHeight = container.clientHeight - 20;
            const chartWidth = container.clientWidth - 20;

            // Create the container
            const chart = document.createElement('div');
            chart.style.width = '100%';
            chart.style.height = '100%';
            chart.style.position = 'relative';
            chart.style.padding = '10px';

            // Create some bars for the placeholder chart
            const barCount = 14;
            for (let i = 0; i < barCount; i++) {
                const isPositive = Math.random() > 0.3;

                // Calculate random height
                const barHeight = 20 + Math.random() * 120;

                // Create the bar
                const bar = document.createElement('div');
                bar.style.position = 'absolute';
                bar.style.bottom = isPositive ? '50%' : `calc(50% - ${barHeight}px)`;
                bar.style.left = `${(i / barCount) * 100}%`;
                bar.style.width = `${80 / barCount}%`;
                bar.style.height = `${barHeight}px`;
                bar.style.backgroundColor = isPositive ? 'rgba(59, 130, 246, 0.7)' : 'rgba(239, 68, 68, 0.7)';
                bar.style.borderRadius = '3px';
                bar.style.transition = 'all 0.3s ease';

                chart.appendChild(bar);
            }

            // Add a center line
            const centerLine = document.createElement('div');
            centerLine.style.position = 'absolute';
            centerLine.style.left = '0';
            centerLine.style.right = '0';
            centerLine.style.top = '50%';
            centerLine.style.height = '1px';
            centerLine.style.backgroundColor = 'rgba(255, 255, 255, 0.2)';

            chart.appendChild(centerLine);
            container.appendChild(chart);
        };

        renderPlaceholderChart();

        // Re-render on window resize
        const handleResize = () => {
            renderPlaceholderChart();
        };

        window.addEventListener('resize', handleResize);
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    return (
        <motion.div
            className="w-full h-[300px] relative"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
        >
            <div ref={chartRef} className="w-full h-full"></div>

            {/* Labels */}
            <div className="absolute left-0 top-[calc(50%-20px)] text-xs text-lightText/50">Bearish</div>
            <div className="absolute left-0 bottom-0 text-xs text-lightText/50">Bullish</div>
            <div className="absolute right-4 bottom-0 text-xs text-lightText/50">14 days</div>
        </motion.div>
    );
};

export default SentimentChart; 