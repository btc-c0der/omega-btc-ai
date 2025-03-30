import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import SentimentChart from './SentimentChart';
import NewsFeed from './NewsFeed';
import MetricCard from '../common/MetricCard';
import CosmicCycleWidget from './CosmicCycleWidget';

const DashboardPage = () => {
    const [sentiment, setSentiment] = useState(0);
    const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
    const [metrics, setMetrics] = useState({
        btcPrice: 0,
        sentimentScore: 0,
        newsCount: 0,
        fearGreedIndex: 0
    });

    // Simulated data fetch
    useEffect(() => {
        // In a real app, this would be an API call
        const fetchData = () => {
            // Simulate API response
            const mockData = {
                btcPrice: 65432.12,
                sentimentScore: Math.random() * 100 - 50, // -50 to 50
                newsCount: Math.floor(Math.random() * 30) + 50, // 50 to 80
                fearGreedIndex: Math.floor(Math.random() * 100)
            };

            setMetrics(mockData);
            setSentiment(mockData.sentimentScore);
            setLastUpdated(new Date());
        };

        fetchData();
        const interval = setInterval(fetchData, 30000); // Every 30 seconds

        return () => clearInterval(interval);
    }, []);

    // Calculate sentiment class
    const getSentimentClass = () => {
        if (sentiment > 25) return "text-success";
        if (sentiment > 0) return "text-primary";
        if (sentiment > -25) return "text-warning";
        return "text-danger";
    };

    // Format price with commas
    const formatPrice = (price: number) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(price);
    };

    return (
        <div className="space-y-6">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
                <p className="text-lightText/70">
                    Market sentiment and latest crypto news analysis by OMEGA
                    {lastUpdated && (
                        <span className="text-xs ml-2">
                            Last updated: {lastUpdated.toLocaleTimeString()}
                        </span>
                    )}
                </p>
            </motion.div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <MetricCard
                    title="Bitcoin Price"
                    value={formatPrice(metrics.btcPrice)}
                    icon="₿"
                    trend="up"
                    trendValue="2.4%"
                />

                <MetricCard
                    title="Sentiment Score"
                    value={`${metrics.sentimentScore.toFixed(1)}`}
                    icon="🧠"
                    additionalClass={getSentimentClass()}
                />

                <MetricCard
                    title="News Articles"
                    value={metrics.newsCount.toString()}
                    icon="📰"
                />

                <MetricCard
                    title="Fear & Greed"
                    value={`${metrics.fearGreedIndex}/100`}
                    icon="😱"
                    bgClass={`bg-gradient-to-r ${metrics.fearGreedIndex < 25 ? "from-danger to-warning" :
                        metrics.fearGreedIndex < 50 ? "from-warning to-primary" :
                            "from-primary to-success"
                        }`}
                />
            </div>

            {/* Charts, Cosmic Cycle, and Trading Signals */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2">
                    <div className="bg-dark rounded-xl p-4 shadow-lg h-[400px]">
                        <h2 className="text-xl font-semibold mb-4">Sentiment Analysis</h2>
                        <SentimentChart />
                    </div>
                </div>

                <div className="space-y-6">
                    {/* Cosmic Cycle Widget */}
                    <CosmicCycleWidget />

                    <div className="bg-dark rounded-xl p-4 shadow-lg">
                        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                            <span>Trading Signal</span>
                            <span className={`text-sm px-2 py-1 rounded ${sentiment > 0 ? 'bg-success/20 text-success' : 'bg-danger/20 text-danger'}`}>
                                {sentiment > 25 ? 'Strong Buy' :
                                    sentiment > 0 ? 'Buy' :
                                        sentiment > -25 ? 'Sell' : 'Strong Sell'}
                            </span>
                        </h2>

                        <div className="space-y-4">
                            <p className="text-lightText/80">
                                Based on the current market sentiment and news analysis, our AI recommends:
                            </p>

                            <div className={`p-4 rounded-lg border ${sentiment > 0 ? 'border-success/30 bg-success/10' : 'border-danger/30 bg-danger/10'
                                }`}>
                                <h3 className="font-bold mb-2">
                                    {sentiment > 0 ? 'Accumulate Bitcoin' : 'Reduce Exposure'}
                                </h3>
                                <p className="text-sm">
                                    {sentiment > 25 ? 'The market sentiment is extremely positive. Consider increasing your Bitcoin position while maintaining healthy diversification.' :
                                        sentiment > 0 ? 'Sentiment is moderately positive. A measured approach to increasing Bitcoin exposure is suggested.' :
                                            sentiment > -25 ? 'Market sentiment is turning negative. Consider taking some profits or reducing position sizes.' :
                                                'Strong negative sentiment detected. Protecting capital should be a priority. Consider moving to stablecoins.'}
                                </p>
                            </div>

                            <div className="text-xs text-lightText/50 italic">
                                Not financial advice. Always do your own research.
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* News Feed */}
            <div className="bg-dark rounded-xl p-4 shadow-lg">
                <h2 className="text-xl font-semibold mb-4">Latest News Analysis</h2>
                <NewsFeed />
            </div>
        </div>
    );
};

export default DashboardPage; 