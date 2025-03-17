import React, { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Text, Html, Cone, Octahedron } from '@react-three/drei';
import { Box, CircularProgress, Typography } from '@mui/material';
import { SxProps, Theme } from '@mui/material/styles';
import useDataFeed from '../hooks/useDataFeed';
import { TrapData } from '../types/data';

const loadingStyles: SxProps<Theme> = {
    display: 'flex',
    flexDirection: 'column',
    gap: 2,
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

interface TrapPointProps {
    position: [number, number, number];
    color: string;
    data: TrapData;
}

const TrapPoint: React.FC<TrapPointProps> = ({ position, color, data }) => {
    const [hovered, setHovered] = useState(false);
    const intensity = hovered ? 1 : 0.5;
    const scale = hovered ? 1.2 : 1;

    return (
        <group
            position={position}
            onPointerOver={() => setHovered(true)}
            onPointerOut={() => setHovered(false)}
        >
            {data.type === 'bullish' ? (
                // Bullish trap - Upward pointing cone
                <Cone
                    args={[0.3, 0.6, 8]}
                    rotation={[Math.PI, 0, 0]}
                    scale={scale}
                >
                    <meshStandardMaterial
                        color={color}
                        emissive={color}
                        emissiveIntensity={intensity}
                        metalness={0.8}
                        roughness={0.2}
                    />
                </Cone>
            ) : (
                // Bearish trap - Octahedron (diamond shape)
                <Octahedron
                    args={[0.3]}
                    scale={scale}
                >
                    <meshStandardMaterial
                        color={color}
                        emissive={color}
                        emissiveIntensity={intensity}
                        metalness={0.8}
                        roughness={0.2}
                    />
                </Octahedron>
            )}
            {hovered && (
                <Html center>
                    <div style={{
                        background: 'rgba(0, 0, 0, 0.8)',
                        padding: '8px',
                        borderRadius: '4px',
                        color: '#fff',
                        fontSize: '12px',
                        whiteSpace: 'nowrap',
                        border: `1px solid ${color}`,
                        boxShadow: `0 0 10px ${color}`
                    }}>
                        <div>Type: {data.type}</div>
                        <div>Price: ${data.price.toLocaleString()}</div>
                        <div>Volume: {data.volume.toLocaleString()}</div>
                        <div>Time: {new Date(data.timestamp).toLocaleString()}</div>
                        <div>Confidence: {(data.confidence * 100).toFixed(1)}%</div>
                    </div>
                </Html>
            )}
        </group>
    );
};

const TrapPatterns3D: React.FC = () => {
    const { data: traps, isLoading, error } = useDataFeed<TrapData[]>('/api/traps');

    if (isLoading) {
        return (
            <Box sx={loadingStyles}>
                <CircularProgress />
                <Typography variant="body2" color="text.secondary">
                    Loading trap patterns...
                </Typography>
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={errorStyles}>
                {error.message || 'Failed to load trap patterns'}
            </Box>
        );
    }

    if (!traps) {
        return (
            <Box sx={errorStyles}>
                No trap patterns found
            </Box>
        );
    }

    // Calculate ranges for better scaling
    const priceRange = {
        min: Math.min(...traps.map(t => t.price)),
        max: Math.max(...traps.map(t => t.price))
    };
    const volumeRange = {
        min: Math.min(...traps.map(t => t.volume)),
        max: Math.max(...traps.map(t => t.volume))
    };
    const timeRange = {
        min: Math.min(...traps.map(t => new Date(t.timestamp).getTime())),
        max: Math.max(...traps.map(t => new Date(t.timestamp).getTime()))
    };

    // Normalize values to grid scale
    const normalize = (value: number, min: number, max: number, scale: number = 10) => {
        return ((value - min) / (max - min)) * scale - scale / 2;
    };

    return (
        <Canvas style={{ background: '#0a1929' }}>
            <OrbitControls enableDamping />
            <ambientLight intensity={0.5} />
            <pointLight position={[10, 10, 10]} intensity={1} />
            <spotLight
                position={[-10, 10, -10]}
                angle={0.5}
                penumbra={1}
                intensity={0.8}
                castShadow
            />
            <fog attach="fog" args={['#0a1929', 5, 20]} />

            {/* Grid and Axes */}
            <gridHelper args={[10, 10]} position={[0, -5, 0]} />

            {/* Axis Labels */}
            <Text
                position={[6, -4.5, 0]}
                fontSize={0.5}
                color="#fff"
                anchorX="left"
                anchorY="middle"
            >
                Price Range: ${priceRange.min.toLocaleString()} - ${priceRange.max.toLocaleString()}
            </Text>
            <Text
                position={[0, 1, -6]}
                fontSize={0.5}
                color="#fff"
                anchorX="center"
                anchorY="top"
            >
                Volume Range: {volumeRange.min.toLocaleString()} - {volumeRange.max.toLocaleString()}
            </Text>
            <Text
                position={[-6, -4.5, 0]}
                fontSize={0.5}
                color="#fff"
                anchorX="right"
                anchorY="middle"
            >
                Time Range: {new Date(timeRange.min).toLocaleDateString()} - {new Date(timeRange.max).toLocaleDateString()}
            </Text>

            {/* Legend */}
            <Html position={[-5, 4, 0]}>
                <div style={{
                    background: 'rgba(0, 0, 0, 0.8)',
                    padding: '12px',
                    borderRadius: '4px',
                    color: '#fff',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.5)'
                }}>
                    <div style={{ marginBottom: '8px', fontWeight: 'bold' }}>Pattern Types:</div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                        <div style={{
                            width: '12px',
                            height: '20px',
                            clipPath: 'polygon(50% 0%, 100% 100%, 0% 100%)',
                            backgroundColor: '#52c41a'
                        }}></div>
                        <div>Bullish Traps (Upward Cone)</div>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div style={{
                            width: '16px',
                            height: '16px',
                            transform: 'rotate(45deg)',
                            backgroundColor: '#ff4d4f'
                        }}></div>
                        <div>Bearish Traps (Diamond)</div>
                    </div>
                </div>
            </Html>

            {/* Trap Points */}
            {traps.map((trap: TrapData) => (
                <TrapPoint
                    key={trap.id}
                    position={[
                        normalize(trap.price, priceRange.min, priceRange.max),
                        normalize(trap.volume, volumeRange.min, volumeRange.max),
                        normalize(new Date(trap.timestamp).getTime(), timeRange.min, timeRange.max)
                    ]}
                    color={trap.type === 'bullish' ? '#52c41a' : '#ff4d4f'}
                    data={trap}
                />
            ))}
        </Canvas>
    );
};

export default TrapPatterns3D; 