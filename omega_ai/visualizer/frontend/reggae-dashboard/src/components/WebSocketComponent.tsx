import { useEffect, useRef, useState } from 'react';

interface WebSocketComponentProps {
    onData: (data: any) => void;
    onConnectionChange: (connected: boolean) => void;
}

const WebSocketComponent: React.FC<WebSocketComponentProps> = ({
    onData,
    onConnectionChange
}) => {
    const [isConnected, setIsConnected] = useState(false);
    const intervalRef = useRef<number | null>(null);

    // Fetch data from API endpoints instead of using WebSocket
    const fetchData = async () => {
        try {
            // Fetch trap probability
            const trapResponse = await fetch('/api/trap-probability');
            const trapData = await trapResponse.json();

            // Fetch position data
            const positionResponse = await fetch('/api/position');
            const positionData = await positionResponse.json();

            // Combine data
            const combinedData = {
                type: 'update',
                timestamp: new Date().toISOString(),
                trap_probability: trapData,
                position: positionData
            };

            // Update connection status
            if (!isConnected) {
                setIsConnected(true);
                onConnectionChange(true);
            }

            // Pass data to parent component
            onData(combinedData);
        } catch (error) {
            console.error('Error fetching data:', error);

            // Update connection status on error
            if (isConnected) {
                setIsConnected(false);
                onConnectionChange(false);
            }
        }
    };

    useEffect(() => {
        // Fetch data immediately on mount
        fetchData();

        // Set up interval to fetch data every 2 seconds
        const intervalId = window.setInterval(() => {
            fetchData();
        }, 2000);

        intervalRef.current = intervalId;

        // Clean up on unmount
        return () => {
            if (intervalRef.current !== null) {
                clearInterval(intervalRef.current);
            }
        };
    }, []);

    return null; // This component doesn't render anything
};

export default WebSocketComponent;