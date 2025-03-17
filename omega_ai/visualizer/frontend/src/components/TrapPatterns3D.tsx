import React from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Text } from '@react-three/drei';
import { Box, CircularProgress } from '@mui/material';
import { SxProps, Theme } from '@mui/material/styles';
import useDataFeed from '../hooks/useDataFeed';
import { TrapData } from '../types/data';

const loadingStyles: SxProps<Theme> = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%',
    width: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
};

const errorStyles: SxProps<Theme> = {
    ...loadingStyles,
    color: 'error.main'
};

const TrapPatterns3D: React.FC = () => {
    const { data: traps, isLoading, error } = useDataFeed<TrapData[]>('/api/traps');

    if (isLoading) {
        return (
            <Box sx={loadingStyles}>
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={errorStyles}>
                {error.message || 'UNK0WN_3RR0R'}
            </Box>
        );
    }

    if (!traps) {
        return (
            <Box sx={errorStyles}>
                N0_D4T4_F0UND.exe
            </Box>
        );
    }

    return (
        <Canvas style={{ background: '#0a1929' }}>
            <OrbitControls enableDamping />
            <ambientLight intensity={0.5} />
            <pointLight position={[10, 10, 10]} />
            <fog attach="fog" args={['#0a1929', 5, 20]} />

            {/* Grid and Axes */}
            <gridHelper args={[10, 10]} />
            <Text position={[5, 0, 0]} fontSize={0.5} color="#fff">
                Price
            </Text>
            <Text position={[0, 5, 0]} fontSize={0.5} color="#fff">
                Volume
            </Text>
            <Text position={[0, 0, 5]} fontSize={0.5} color="#fff">
                Time
            </Text>

            {/* Trap Points */}
            {traps.map((trap: TrapData) => (
                <mesh
                    key={trap.id}
                    position={[
                        trap.price / 10000, // Scale price to grid size
                        trap.volume / 1000, // Scale volume to grid height
                        new Date(trap.timestamp).getTime() / 86400000 % 10 // Map time to grid depth
                    ]}
                >
                    <sphereGeometry args={[0.2]} />
                    <meshStandardMaterial
                        color={trap.type === 'bullish' ? '#52c41a' : '#ff4d4f'}
                        emissive={trap.type === 'bullish' ? '#52c41a' : '#ff4d4f'}
                        emissiveIntensity={0.5}
                    />
                </mesh>
            ))}
        </Canvas>
    );
};

export default TrapPatterns3D; 