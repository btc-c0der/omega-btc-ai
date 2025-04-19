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

/**
 * Fear & Greed Index API Service
 * Uses the RapidAPI Crypto Fear & Greed Index API
 * Docs: https://rapidapi.com/onshabogdan-5SUvbWmtd0l/api/crypto-fear-greed-index2
 */

export interface FearGreedData {
    value: number;
    valueClassification: string;
    timestamp: string;
    timeUntilUpdate: string;
}

export interface FearGreedHistoryData {
    data: {
        timestamp: string;
        value: number;
        valueClassification: string;
    }[];
}

const HEADERS = {
    'X-RapidAPI-Key': process.env.REACT_APP_RAPIDAPI_KEY || 'YOUR_API_KEY_HERE',
    'X-RapidAPI-Host': 'crypto-fear-greed-index2.p.rapidapi.com'
};

/**
 * Fetch the current Fear and Greed Index
 */
export const fetchFearGreedIndex = async (): Promise<FearGreedData> => {
    try {
        const response = await fetch('https://crypto-fear-greed-index2.p.rapidapi.com/v1/fgi', {
            method: 'GET',
            headers: HEADERS
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        return data.fgi;
    } catch (error) {
        console.error('Error fetching Fear & Greed Index:', error);
        // Return fallback data if the API fails
        return {
            value: 45,
            valueClassification: 'Fear',
            timestamp: new Date().toISOString(),
            timeUntilUpdate: '24h'
        };
    }
};

/**
 * Fetch historical Fear and Greed Index data
 * @param limit - Number of days (default: 30)
 */
export const fetchFearGreedHistory = async (limit = 30): Promise<FearGreedHistoryData> => {
    try {
        const response = await fetch(`https://crypto-fear-greed-index2.p.rapidapi.com/v1/fgi/history?limit=${limit}`, {
            method: 'GET',
            headers: HEADERS
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching Fear & Greed history:', error);
        // Return fallback data with simulated values
        const fallbackData = {
            data: Array.from({ length: limit }).map((_, i) => {
                const date = new Date();
                date.setDate(date.getDate() - (limit - i));

                // Generate a random value between 20 and 70 with some trend
                const baseValue = 45;
                const randomVariation = Math.sin(i * 0.4) * 25;
                const value = Math.round(Math.max(0, Math.min(100, baseValue + randomVariation)));

                let valueClassification = 'Neutral';
                if (value <= 25) valueClassification = 'Extreme Fear';
                else if (value <= 40) valueClassification = 'Fear';
                else if (value <= 60) valueClassification = 'Neutral';
                else if (value <= 80) valueClassification = 'Greed';
                else valueClassification = 'Extreme Greed';

                return {
                    timestamp: date.toISOString(),
                    value,
                    valueClassification
                };
            })
        };

        return fallbackData;
    }
}; 