import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';

interface RedisKey {
    key: string;
    type: string;
    length?: number;
    fields?: number;
}

const RedisFeedMonitor: React.FC = () => {
    const [redisKeys, setRedisKeys] = useState<RedisKey[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
    const [connected, setConnected] = useState(false);

    useEffect(() => {
        // Function to fetch Redis keys
        const fetchRedisKeys = async () => {
            try {
                const response = await axios.get('/api/redis-keys');
                if (response.data && response.data.keys) {
                    setRedisKeys(response.data.keys);
                    setLastUpdated(new Date());
                    setConnected(true);
                    setError(null);
                } else {
                    setError('Invalid response format');
                }
            } catch (err) {
                console.error('Error fetching Redis keys:', err);
                setError('Failed to connect to Redis');
                setConnected(false);
            } finally {
                setLoading(false);
            }
        };

        // Initial fetch
        fetchRedisKeys();

        // Set up polling
        const intervalId = setInterval(fetchRedisKeys, 10000); // Poll every 10 seconds

        return () => clearInterval(intervalId);
    }, []);

    // Get relative time
    const getRelativeTime = (date: Date | null) => {
        if (!date) return '';

        const now = new Date();
        const diffSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

        if (diffSeconds < 10) return 'Just now';
        if (diffSeconds < 60) return `${diffSeconds} seconds ago`;
        if (diffSeconds < 120) return '1 minute ago';

        const diffMinutes = Math.floor(diffSeconds / 60);
        if (diffMinutes < 60) return `${diffMinutes} minutes ago`;

        return date.toLocaleTimeString();
    };

    // Format key for display
    const formatKey = (key: string) => {
        // Truncate long keys but keep important parts
        if (key.length > 35) {
            const parts = key.split(':');
            if (parts.length > 1) {
                return `${parts[0]}:...:${parts[parts.length - 1]}`;
            }
            return `${key.substring(0, 15)}...${key.substring(key.length - 15)}`;
        }
        return key;
    };

    // Get appropriate icon for Redis type
    const getTypeIcon = (type: string) => {
        switch (type) {
            case 'string': return '📄';
            case 'list': return '📋';
            case 'hash': return '🔑';
            case 'set': return '🔢';
            case 'zset': return '📊';
            default: return '❓';
        }
    };

    // Filter and sort keys for display
    const getDisplayKeys = () => {
        if (!redisKeys.length) return [];

        // Sort keys by name
        return redisKeys
            .filter(key => !key.key.startsWith('internal:'))
            .sort((a, b) => a.key.localeCompare(b.key))
            .slice(0, 15); // Show max 15 keys
    };

    const displayKeys = getDisplayKeys();

    return (
        <div className="bg-reggae-black-light p-4 rounded-lg border border-reggae-gold/20">
            <div className="flex justify-between items-center mb-3">
                <h2 className="text-xl font-display text-reggae-gold">REDIS FEED</h2>
                <div className="flex items-center">
                    <div className={`h-2 w-2 rounded-full ${connected ? 'bg-reggae-green' : 'bg-reggae-red'} mr-2`}></div>
                    <span className="text-xs text-reggae-text/70">
                        {connected ? 'Connected' : 'Disconnected'}
                    </span>
                </div>
            </div>

            {loading ? (
                <div className="flex justify-center items-center h-48">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-reggae-gold"></div>
                </div>
            ) : error ? (
                <div className="bg-reggae-red/10 p-3 rounded-lg border border-reggae-red/30 text-center text-reggae-red">
                    {error}
                </div>
            ) : displayKeys.length === 0 ? (
                <div className="text-center p-4 text-reggae-text/50">
                    No Redis keys found
                </div>
            ) : (
                <>
                    <div className="space-y-2 max-h-60 overflow-y-auto custom-scrollbar mb-2">
                        {displayKeys.map((keyData, index) => (
                            <motion.div
                                key={keyData.key}
                                className="p-2 bg-reggae-black rounded text-sm border border-reggae-gold/10 flex justify-between"
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.05 }}
                            >
                                <div className="flex items-center overflow-hidden">
                                    <span className="mr-2">{getTypeIcon(keyData.type)}</span>
                                    <span className="text-xs font-mono text-reggae-electric-blue truncate" title={keyData.key}>
                                        {formatKey(keyData.key)}
                                    </span>
                                </div>
                                <div className="text-xs text-reggae-text/60 flex items-center">
                                    {keyData.type === 'string' && keyData.length !== undefined &&
                                        <span>{keyData.length} chars</span>}
                                    {keyData.type === 'list' && keyData.length !== undefined &&
                                        <span>{keyData.length} items</span>}
                                    {keyData.type === 'hash' && keyData.fields !== undefined &&
                                        <span>{keyData.fields} fields</span>}
                                </div>
                            </motion.div>
                        ))}
                    </div>

                    <div className="text-right text-xs text-reggae-text/50 italic mt-2">
                        Updated {getRelativeTime(lastUpdated)}
                    </div>
                </>
            )}

            {/* Custom scrollbar style */}
            <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #1E1E1E;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #FFD700;
          border-radius: 10px;
        }
      `}</style>
        </div>
    );
};

export default RedisFeedMonitor; 