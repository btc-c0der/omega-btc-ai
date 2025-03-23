import React, { useState, useEffect } from 'react';
import { WebSocket } from 'ws';
import styled, { DefaultTheme } from 'styled-components';

interface TraderPersona {
    profile: string;
    name: string;
    capital: number;
    pnl: number;
    winRate: number;
    emotionalState: string;
    divineConnection: number;
    riskLevel: number;
    confidence: number;
    enlightenedTrades: number;
    positions: Position[];
}

interface Position {
    size: number;
    entryPrice: number;
    currentPrice: number;
    pnl: number;
    liquidationPrice: number;
    takeProfit: number;
    stopLoss: number;
}

interface TraderPersonaPanelProps {
    websocketUrl: string;
}

const profileColors: Record<string, string> = {
    strategic: '#4CAF50',  // Green
    aggressive: '#F44336', // Red
    newbie: '#2196F3',    // Blue
    scalper: '#FF9800',   // Orange
    yolo: '#9C27B0'       // Purple
};

const profileEmojis: Record<string, string> = {
    strategic: '🎯',
    aggressive: '🔥',
    newbie: '🌱',
    scalper: '⚡',
    yolo: '🎲'
};

const emotionColors: Record<string, string> = {
    neutral: '#607D8B',
    mindful: '#4CAF50',
    zen: '#00BCD4',
    enlightened: '#9C27B0',
    fearful: '#F44336',
    greedy: '#FF9800',
    fomo: '#E91E63'
};

const Panel = styled.div`
  padding: 20px;
  background: #1a1a1a;
  border-radius: 10px;
  color: #fff;
`;

const ConnectionStatus = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
`;

const StatusDot = styled.span<{ connected: boolean }>`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: ${props => props.connected ? '#4CAF50' : '#F44336'};
`;

const TradersGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
`;

const TraderCard = styled.div<{ borderColor: string }>`
  background: #2a2a2a;
  border-radius: 8px;
  padding: 15px;
  border: 2px solid ${props => props.borderColor};
`;

const TraderHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
`;

const ProfileEmoji = styled.span`
  font-size: 24px;
`;

const EmotionalState = styled.span<{ bgColor: string }>`
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  text-transform: uppercase;
  background-color: ${props => props.bgColor};
`;

const TraderStats = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-bottom: 15px;
`;

const Stat = styled.div`
  background: #333;
  padding: 8px;
  border-radius: 4px;
`;

const StatLabel = styled.label`
  font-size: 12px;
  color: #888;
`;

const StatValue = styled.span<{ isProfit?: boolean }>`
  display: block;
  font-size: 16px;
  font-weight: bold;
  color: ${props => props.isProfit === undefined ? 'inherit' : props.isProfit ? '#4CAF50' : '#F44336'};
`;

const DivineMeters = styled.div`
  margin-bottom: 15px;
`;

const Meter = styled.div`
  margin-bottom: 8px;
`;

const MeterLabel = styled.label`
  display: block;
  font-size: 12px;
  margin-bottom: 4px;
`;

const MeterBar = styled.div`
  height: 8px;
  background: #333;
  border-radius: 4px;
  overflow: hidden;
`;

const MeterFill = styled.div<{ width: string; bgColor: string }>`
  height: 100%;
  width: ${props => props.width};
  background-color: ${props => props.bgColor};
  transition: width 0.3s ease;
`;

const MeterValue = styled.span`
  font-size: 12px;
  color: #888;
`;

const Positions = styled.div`
  background: #333;
  padding: 10px;
  border-radius: 4px;
`;

const PositionTitle = styled.h4`
  margin: 0 0 10px;
  font-size: 14px;
`;

const NoPositions = styled.p`
  color: #888;
  font-style: italic;
  text-align: center;
`;

const Position = styled.div`
  background: #2a2a2a;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 8px;
  &:last-child {
    margin-bottom: 0;
  }
`;

const PositionHeader = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
`;

const PositionDetails = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  font-size: 12px;
`;

const PositionTargets = styled(PositionDetails)`
  margin-top: 8px;
  grid-template-columns: repeat(2, 1fr);
`;

export const TraderPersonaPanel: React.FC<TraderPersonaPanelProps> = ({ websocketUrl }) => {
    const [traders, setTraders] = useState<TraderPersona[]>([]);
    const [connected, setConnected] = useState(false);

    useEffect(() => {
        const ws = new WebSocket(websocketUrl);

        ws.onopen = () => {
            console.log('Connected to trader personas websocket');
            setConnected(true);
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data.toString());
                setTraders(data.traders);
            } catch (error) {
                console.error('Error parsing websocket message:', error);
            }
        };

        ws.onclose = () => {
            console.log('Disconnected from trader personas websocket');
            setConnected(false);
        };

        return () => {
            ws.close();
        };
    }, [websocketUrl]);

    const renderDivineMeters = (trader: TraderPersona) => (
        <DivineMeters>
            <Meter>
                <MeterLabel>Divine Connection</MeterLabel>
                <MeterBar>
                    <MeterFill
                        width={`${trader.divineConnection * 100}%`}
                        bgColor="#9C27B0"
                    />
                </MeterBar>
                <MeterValue>{(trader.divineConnection * 100).toFixed(1)}%</MeterValue>
            </Meter>

            <Meter>
                <MeterLabel>Confidence</MeterLabel>
                <MeterBar>
                    <MeterFill
                        width={`${trader.confidence * 100}%`}
                        bgColor="#2196F3"
                    />
                </MeterBar>
                <MeterValue>{(trader.confidence * 100).toFixed(1)}%</MeterValue>
            </Meter>

            <Meter>
                <MeterLabel>Risk Level</MeterLabel>
                <MeterBar>
                    <MeterFill
                        width={`${trader.riskLevel * 100}%`}
                        bgColor={trader.riskLevel > 0.7 ? '#F44336' : '#4CAF50'}
                    />
                </MeterBar>
                <MeterValue>{(trader.riskLevel * 100).toFixed(1)}%</MeterValue>
            </Meter>
        </DivineMeters>
    );

    const renderPositions = (positions: Position[]) => (
        <Positions>
            <PositionTitle>Active Positions</PositionTitle>
            {positions.length === 0 ? (
                <NoPositions>No active positions</NoPositions>
            ) : (
                positions.map((position, index) => (
                    <Position key={index}>
                        <PositionHeader>
                            <span>Size: {position.size} BTC</span>
                            <StatValue isProfit={position.pnl >= 0}>
                                PnL: ${position.pnl.toFixed(2)}
                            </StatValue>
                        </PositionHeader>
                        <PositionDetails>
                            <div>Entry: ${position.entryPrice.toFixed(2)}</div>
                            <div>Current: ${position.currentPrice.toFixed(2)}</div>
                            <div>Liq: ${position.liquidationPrice.toFixed(2)}</div>
                        </PositionDetails>
                        <PositionTargets>
                            <div>TP: ${position.takeProfit.toFixed(2)}</div>
                            <div>SL: ${position.stopLoss.toFixed(2)}</div>
                        </PositionTargets>
                    </Position>
                ))
            )}
        </Positions>
    );

    return (
        <Panel>
            <ConnectionStatus>
                <StatusDot connected={connected} />
                {connected ? 'Connected' : 'Disconnected'}
            </ConnectionStatus>

            <TradersGrid>
                {traders.map((trader) => (
                    <TraderCard
                        key={trader.profile}
                        borderColor={profileColors[trader.profile]}
                    >
                        <TraderHeader>
                            <ProfileEmoji>{profileEmojis[trader.profile]}</ProfileEmoji>
                            <h3>{trader.name}</h3>
                            <EmotionalState bgColor={emotionColors[trader.emotionalState]}>
                                {trader.emotionalState}
                            </EmotionalState>
                        </TraderHeader>

                        <TraderStats>
                            <Stat>
                                <StatLabel>Capital</StatLabel>
                                <StatValue>${trader.capital.toFixed(2)}</StatValue>
                            </Stat>
                            <Stat>
                                <StatLabel>PnL</StatLabel>
                                <StatValue isProfit={trader.pnl >= 0}>
                                    ${trader.pnl.toFixed(2)}
                                </StatValue>
                            </Stat>
                            <Stat>
                                <StatLabel>Win Rate</StatLabel>
                                <StatValue>{(trader.winRate * 100).toFixed(1)}%</StatValue>
                            </Stat>
                            <Stat>
                                <StatLabel>Enlightened Trades</StatLabel>
                                <StatValue>{trader.enlightenedTrades}</StatValue>
                            </Stat>
                        </TraderStats>

                        {renderDivineMeters(trader)}
                        {renderPositions(trader.positions)}
                    </TraderCard>
                ))}
            </TradersGrid>
        </Panel>
    );
}; 