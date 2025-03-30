import React, { useEffect, useRef } from 'react';
import { Box, Typography, Paper, Grid } from '@mui/material';
import * as THREE from 'three';
import { useThree, Canvas } from '@react-three/fiber';
import { OrbitControls, Text } from '@react-three/drei';

const MemoryParticles = () => {
    const { camera } = useThree();
    const particlesRef = useRef<THREE.Points>(null);

    useEffect(() => {
        camera.position.z = 5;
    }, [camera]);

    const particleCount = 1000;
    const positions = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i++) {
        positions[i * 3] = (Math.random() - 0.5) * 10;
        positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
        positions[i * 3 + 2] = (Math.random() - 0.5) * 10;
    }

    return (
        <points ref={particlesRef}>
            <bufferGeometry>
                <bufferAttribute
                    attach="attributes-position"
                    count={particleCount}
                    array={positions}
                    itemSize={3}
                />
            </bufferGeometry>
            <pointsMaterial
                size={0.02}
                color="#00ff88"
                transparent
                opacity={0.6}
            />
        </points>
    );
};

const ImmortalMemoryArchitect: React.FC = () => {
    return (
        <Box sx={{ height: '100%', position: 'relative' }}>
            <Typography
                variant="h4"
                sx={{
                    position: 'absolute',
                    top: 20,
                    left: 20,
                    zIndex: 1,
                    color: '#00ff88',
                    textShadow: '0 0 10px rgba(0,255,136,0.5)',
                    fontWeight: 'bold',
                }}
            >
                The Architect of Immortal Memory
            </Typography>

            <Grid container spacing={2} sx={{ height: '100%', p: 2 }}>
                <Grid item xs={12} md={8}>
                    <Paper
                        sx={{
                            height: '100%',
                            background: 'rgba(10, 14, 23, 0.8)',
                            backdropFilter: 'blur(10px)',
                            border: '1px solid rgba(0, 255, 136, 0.2)',
                            p: 3,
                        }}
                    >
                        <Box sx={{ height: '100%', position: 'relative' }}>
                            <Canvas>
                                <OrbitControls enableZoom={false} />
                                <ambientLight intensity={0.5} />
                                <pointLight position={[10, 10, 10]} />
                                <MemoryParticles />
                                <Text
                                    position={[0, 0, 0]}
                                    fontSize={0.5}
                                    color="#00ff88"
                                    anchorX="center"
                                    anchorY="middle"
                                >
                                    OMEGA MEMORY
                                </Text>
                            </Canvas>
                        </Box>
                    </Paper>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Paper
                        sx={{
                            height: '100%',
                            background: 'rgba(10, 14, 23, 0.8)',
                            backdropFilter: 'blur(10px)',
                            border: '1px solid rgba(0, 255, 136, 0.2)',
                            p: 3,
                        }}
                    >
                        <Typography
                            variant="h6"
                            sx={{
                                color: '#00ff88',
                                mb: 2,
                                fontFamily: 'monospace',
                            }}
                        >
                            Memory Statistics
                        </Typography>
                        <Box
                            sx={{
                                display: 'flex',
                                flexDirection: 'column',
                                gap: 2,
                            }}
                        >
                            {/* Add memory statistics here */}
                            <Typography variant="body1" color="text.secondary">
                                Total Memory Blocks: 1,337
                            </Typography>
                            <Typography variant="body1" color="text.secondary">
                                Active Neural Pathways: 42
                            </Typography>
                            <Typography variant="body1" color="text.secondary">
                                Memory Integrity: 99.9%
                            </Typography>
                        </Box>
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
};

export default ImmortalMemoryArchitect; 