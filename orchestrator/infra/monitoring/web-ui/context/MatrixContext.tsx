import React, { createContext, useContext, useState, useEffect } from 'react';

interface MatrixData {
    testRate: number;
    testFailures: number;
    redisCommands: number;
    marketTrends: number;
    serviceHealth: number;
    testCoverage: number;
}

interface MatrixContextType {
    data: MatrixData | null;
    loading: boolean;
    error: string | null;
    refreshData: () => Promise<void>;
}

const MatrixContext = createContext<MatrixContextType | undefined>(undefined);

export const MatrixProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [data, setData] = useState<MatrixData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = async () => {
        try {
            setLoading(true);
            setError(null);

            const response = await fetch('http://localhost:8080/api/matrix/metrics');
            if (!response.ok) {
                throw new Error('Failed to fetch Matrix metrics');
            }

            const metrics = await response.json();
            setData(metrics);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();

        // Set up polling interval
        const interval = setInterval(fetchData, 5000);

        return () => clearInterval(interval);
    }, []);

    return (
        <MatrixContext.Provider value={{ data, loading, error, refreshData: fetchData }}>
            {children}
        </MatrixContext.Provider>
    );
};

export const useMatrix = () => {
    const context = useContext(MatrixContext);
    if (context === undefined) {
        throw new Error('useMatrix must be used within a MatrixProvider');
    }
    return context;
}; 