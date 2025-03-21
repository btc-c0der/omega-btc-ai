from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT
import asyncio
import os
import json
import redis

async def check_positions():
    # Get API credentials from .env
    api_key = os.environ.get('BITGET_API_KEY', '')
    secret_key = os.environ.get('BITGET_SECRET_KEY', '')
    passphrase = os.environ.get('BITGET_PASSPHRASE', '')
    sub_account = os.environ.get('STRATEGIC_SUB_ACCOUNT_NAME', '')
    
    # Force expected leverage to 11 as requested by user (instead of .env value)
    expected_leverage = 11  # Manually set to 11x
    
    print(f'Using API key: {api_key[:5]}...')
    print(f'Using sub-account: {sub_account}')
    print(f'Expected leverage: {expected_leverage}x')
    
    # Initialize BitGet client
    client = BitGetCCXT(
        api_key=api_key,
        api_secret=secret_key,
        password=passphrase,
        use_testnet=False,
        sub_account=sub_account
    )
    
    try:
        # Initialize the client
        await client.initialize()
        
        # Get positions for BTC
        positions = await client.get_positions('BTC/USDT:USDT')
        print(f'Found {len(positions)} positions')
        
        # Print position details
        for pos in positions:
            print(json.dumps(pos, indent=2))
            
        # Store position in Redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        
        # Check if any positions are active
        active_positions = [p for p in positions if float(p.get('contracts', 0)) > 0]
        
        if active_positions:
            # Convert to dashboard format
            position = active_positions[0]
            
            # Get actual leverage from exchange
            actual_leverage = int(position.get('leverage', 1))
            
            # Check if there's a discrepancy
            leverage_mismatch = actual_leverage != expected_leverage
            
            formatted_position = {
                'has_position': True,
                'position_side': position.get('side', '').lower(),
                'entry_price': float(position.get('entryPrice', 0)),
                'current_price': float(position.get('markPrice', 0)) if position.get('markPrice') else 0,
                'position_size': float(position.get('contracts', 0)),
                'leverage': actual_leverage,  # Store actual leverage from exchange
                'expected_leverage': expected_leverage,  # Store expected leverage from .env
                'leverage_mismatch': leverage_mismatch,  # Flag to show alert in UI
                'risk_multiplier': 1.0,  # Default
                'pnl_percent': float(position.get('percentage', 0)) if position.get('percentage') else 0,
                'pnl_usd': float(position.get('unrealizedPnl', 0)) if position.get('unrealizedPnl') else 0,
                'stop_loss': float(position.get('stopLossPrice', 0)) if position.get('stopLossPrice') else 0,
                'entry_time': position.get('timestamp', ''),
                'source': 'bitget',
                'timestamp': position.get('timestamp', '')
            }
            
            # Recalculate PnL based on our expected leverage value
            # Initialize variables to avoid linter errors
            pnlPercent = 0.0
            pnlUsd = 0.0
            
            if position.get('entryPrice') and position.get('markPrice'):
                entryPrice = float(position.get('entryPrice', 0))
                currentPrice = float(position.get('markPrice', 0))
                positionSize = float(position.get('contracts', 0))
                side = position.get('side', '').lower()
                
                # Use actual leverage for calculations as that's what the exchange uses
                if side == 'long':
                    pnlPercent = ((currentPrice - entryPrice) / entryPrice) * 100 * actual_leverage
                    pnlUsd = (currentPrice - entryPrice) * positionSize * actual_leverage
                elif side == 'short':
                    pnlPercent = ((entryPrice - currentPrice) / entryPrice) * 100 * actual_leverage
                    pnlUsd = (entryPrice - currentPrice) * positionSize * actual_leverage
                
                # Update the formatted position with recalculated values
                formatted_position['pnl_percent'] = pnlPercent
                formatted_position['pnl_usd'] = pnlUsd
            
            # Store in Redis
            r.set('current_position', json.dumps(formatted_position))
            print(f'Stored position data in Redis with leverage details:')
            print(f'  Actual leverage (from exchange): {actual_leverage}x')
            print(f'  Expected leverage (from .env): {expected_leverage}x')
            if leverage_mismatch:
                print(f'  ⚠️ ALERT: Leverage values do not match!')
        else:
            # Store empty position
            r.set('current_position', json.dumps({'has_position': False, 'timestamp': ''}))
            print(f'No active positions found, stored empty position in Redis')
        
    except Exception as e:
        print(f'Error: {str(e)}')
    finally:
        # Close the client
        await client.close()

if __name__ == "__main__":
    asyncio.run(check_positions()) 