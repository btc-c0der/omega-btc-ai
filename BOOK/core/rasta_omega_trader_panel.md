# RASTA OMEGA TRADER Panel Documentation

## Overview

The RASTA OMEGA TRADER is a specialized trading interface component within the OMEGA BTC AI dashboard. It provides real-time trading information and position management capabilities with a unique Rastafarian theme.

## Location

- Found within the BitGet card interface in the main dashboard
- Part of the trading control section

## Component Details

### 1. Header Component

```html
<h2>
    <span><i class="fas fa-rocket"></i> RASTA OMEGA TRADER</span>
    <span class="position-badge short" id="bg-position-badge">
        <i class="fas fa-arrow-down"></i> SHORT
    </span>
</h2>
```

**Functionality:**

- Displays trading panel title with rocket icon
- Shows current position type (SHORT/LONG) with directional arrows
- Dynamic badge color based on position type (red for short, green for long)

### 2. PnL (Profit and Loss) Display

```html
<div class="bitget-pnl-box">
    <div class="bitget-pnl-item">
        <div class="bitget-pnl-label">PNL %</div>
        <div class="bitget-pnl-value negative" id="bg-pnl-percent">-0.66%</div>
    </div>
    <div class="bitget-pnl-item">
        <div class="bitget-pnl-label">PNL $</div>
        <div class="bitget-pnl-value negative" id="bg-pnl-usd">-$0.32</div>
    </div>
</div>
```

**Features:**

- Real-time PnL updates in both percentage and USD
- Color-coded values (green for profit, red for loss)
- Dynamic updates via WebSocket connection
- Automatic formatting of values with proper decimals

### 3. Position Statistics Grid

```html
<div class="bitget-stats">
    <div class="bitget-stat-box highlight">
        <div class="bitget-stat-label">SIZE</div>
        <div class="bitget-stat-value" id="bg-position-size">0.0113 BTC</div>
    </div>
    <div class="bitget-stat-box">
        <div class="bitget-stat-label">LEVERAGE</div>
        <div class="bitget-stat-value" id="bg-leverage">20x</div>
    </div>
    <div class="bitget-stat-box">
        <div class="bitget-stat-label">MARGIN</div>
        <div class="bitget-stat-value" id="bg-margin">$47.58</div>
    </div>
</div>
```

**Key Metrics:**

- Position Size: Current trading position in BTC
- Leverage: Current leverage multiplier with warning indicators for mismatches
- Margin: Current margin amount in USD

### 4. Detailed Position Information

```html
<div class="bitget-detail-grid">
    <!-- Entry and Current Prices -->
    <div class="bitget-detail-row">
        <div class="bitget-detail-label">ENTRY PRICE</div>
        <div class="bitget-detail-value" id="bg-entry-price">$84,205.22</div>
    </div>
    <!-- Break-even and Liquidation -->
    <div class="bitget-detail-row">
        <div class="bitget-detail-label">BREAK-EVEN</div>
        <div class="bitget-detail-value" id="bg-breakeven">$83,798.22</div>
    </div>
    <!-- Trading Modes -->
    <div class="bitget-detail-row">
        <div class="bitget-detail-label">MARGIN MODE</div>
        <div class="bitget-detail-value" id="bg-margin-mode">CROSSED</div>
    </div>
</div>
```

**Information Displayed:**

- Entry Price: Initial position entry price
- Current Price: Live market price
- Break-even Point: Price needed for zero PnL
- Liquidation Price: Position liquidation threshold
- Margin Mode: CROSSED or ISOLATED
- Position Mode: ONE-WAY or HEDGE

### 5. Risk Management Controls

```html
<div class="bitget-take-profit" id="bg-tp-container">
    <div>
        <span class="bitget-order-dot tp"></span>
        <span class="bitget-detail-label">TAKE PROFIT</span>
    </div>
    <div class="bitget-detail-value" id="bg-take-profit">$83,500.00</div>
</div>
```

**Features:**

- Take Profit settings with visual indicators
- Stop Loss configuration with safety thresholds
- Visual dots indicating order types (TP/SL)
- Real-time price target updates

## Technical Implementation

> 🔗 For detailed information about BitGet data management and real-time updates, see [BitGet Data Management & Real-time Updates](./bitget_data_management.md)
> 🔗 For comprehensive documentation on BitGet mainnet integration, see [BitGet Mainnet Integration Flow](./bitget_mainnet_integration.md)

### State Management

```javascript
// Position side update logic
if (side.toLowerCase() === 'long') {
    sideElement.innerHTML = `${formattedSide} ↑`;
    sideElement.className = 'value positive';
} else if (side.toLowerCase() === 'short') {
    sideElement.innerHTML = `${formattedSide} ↓`;
    sideElement.className = 'value negative';
}

// Leverage warning system
if (positionData.expected_leverage !== undefined && positionData.leverage_mismatch) {
    leverageElement.innerHTML = `${leverage}x <span class="warning" title="Expected: ${positionData.expected_leverage}x">⚠️</span>`;
    leverageElement.style.color = '#ff9900';
}
```

### Real-time Updates

- WebSocket connection for live data feeds
- Automatic PnL calculations
- Position status monitoring
- Price feed integration
- Error state management

### Error Handling

- Comprehensive error states for all components
- Visual feedback for connection issues
- Fallback displays for missing data
- Automatic reconnection logic

## Styling Details

### Theme Elements

- Rastafarian color palette:
  - Green: #00B52D (profits/long positions)
  - Red: #FF3D00 (losses/short positions)
  - Yellow: #FFD700 (warnings/notifications)
- Custom fonts and icons
- Responsive grid layouts
- Interactive hover states

### Visual Indicators

- Position badges with directional arrows
- Color-coded PnL displays
- Warning indicators for risk levels
- Status dots for order types
- Dynamic updates with smooth transitions

## Future Enhancements

- Multi-pair trading support
- Advanced order types integration
- Custom alert configurations
- Performance metrics dashboard
- Risk management presets
- Trading strategy integration
- Historical performance analytics
