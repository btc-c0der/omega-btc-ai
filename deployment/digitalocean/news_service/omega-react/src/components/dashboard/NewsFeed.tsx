import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface NewsItem {
    id: string;
    title: string;
    source: string;
    timestamp: string;
    url: string;
    sentiment: number;
    summary: string;
}

const NewsFeed = () => {
    const [newsItems, setNewsItems] = useState<NewsItem[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        // Mock API call
        const fetchNews = async () => {
            setLoading(true);

            // Simulate API delay
            await new Promise(resolve => setTimeout(resolve, 1000));

            // Mock data
            const mockNewsItems: NewsItem[] = [
                {
                    id: '1',
                    title: 'Bitcoin Breaks $65K as Institutional Adoption Soars',
                    source: 'CryptoNews',
                    timestamp: '2 hours ago',
                    url: '#',
                    sentiment: 42,
                    summary: 'Bitcoin surged past $65,000 as major financial institutions announce new crypto offerings, sparking renewed bullish sentiment across the market.'
                },
                {
                    id: '2',
                    title: 'New Regulatory Framework for Cryptocurrencies Proposed',
                    source: 'Financial Times',
                    timestamp: '5 hours ago',
                    url: '#',
                    sentiment: -15,
                    summary: 'A new regulatory framework has been proposed that could impact how cryptocurrencies are traded and taxed, raising concerns among some market participants.'
                },
                {
                    id: '3',
                    title: 'Lightning Network Transactions Hit All-Time High',
                    source: 'Bitcoin Magazine',
                    timestamp: '7 hours ago',
                    url: '#',
                    sentiment: 38,
                    summary: 'Bitcoin\'s Layer 2 solution sees unprecedented adoption with daily transactions reaching new highs, demonstrating growing interest in fast, low-fee payments.'
                },
                {
                    id: '4',
                    title: 'Mining Difficulty Adjusts Upward by 8%',
                    source: 'CoinDesk',
                    timestamp: '10 hours ago',
                    url: '#',
                    sentiment: 5,
                    summary: 'Bitcoin mining difficulty has increased significantly, reflecting the growing computational power dedicated to securing the network.'
                },
                {
                    id: '5',
                    title: 'El Salvador Adds 100 More BTC to National Reserve',
                    source: 'Bitcoin News',
                    timestamp: '1 day ago',
                    url: '#',
                    sentiment: 28,
                    summary: 'The first country to adopt Bitcoin as legal tender continues to accumulate, citing long-term confidence in the cryptocurrency\'s value proposition.'
                }
            ];

            setNewsItems(mockNewsItems);
            setLoading(false);
        };

        fetchNews();
    }, []);

    // Get sentiment class based on score
    const getSentimentClass = (sentiment: number) => {
        if (sentiment > 25) return "bg-success/20 text-success";
        if (sentiment > 0) return "bg-primary/20 text-primary";
        if (sentiment > -25) return "bg-warning/20 text-warning";
        return "bg-danger/20 text-danger";
    };

    // Get sentiment label based on score
    const getSentimentLabel = (sentiment: number) => {
        if (sentiment > 25) return "Very Bullish";
        if (sentiment > 0) return "Bullish";
        if (sentiment > -25) return "Bearish";
        return "Very Bearish";
    };

    return (
        <div className="space-y-4">
            {loading ? (
                <div className="flex justify-center py-8">
                    <motion.div
                        className="h-12 w-12 rounded-full border-4 border-primary border-t-transparent"
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    />
                </div>
            ) : (
                <AnimatePresence>
                    {newsItems.map((item, index) => (
                        <motion.div
                            key={item.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, height: 0 }}
                            transition={{ duration: 0.3, delay: index * 0.1 }}
                            className="bg-dark/50 rounded-lg p-4 hover:bg-dark/80 transition-colors"
                        >
                            <div className="flex justify-between items-start">
                                <div>
                                    <h3 className="font-medium text-lg">{item.title}</h3>
                                    <div className="flex items-center gap-2 text-xs opacity-70 mt-1">
                                        <span>{item.source}</span>
                                        <span>•</span>
                                        <span>{item.timestamp}</span>
                                    </div>
                                </div>
                                <div className={`px-2 py-1 rounded text-xs ${getSentimentClass(item.sentiment)}`}>
                                    {getSentimentLabel(item.sentiment)}
                                </div>
                            </div>

                            <p className="mt-2 text-sm opacity-90">{item.summary}</p>

                            <div className="flex justify-between items-center mt-3 pt-2 border-t border-dark/30">
                                <a href={item.url} className="text-xs text-primary hover:underline">
                                    Read full article →
                                </a>
                                <div className="flex items-center gap-3">
                                    <button className="text-xs hover:text-primary transition-colors">
                                        Save
                                    </button>
                                    <button className="text-xs hover:text-primary transition-colors">
                                        Share
                                    </button>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>
            )}
        </div>
    );
};

export default NewsFeed; 