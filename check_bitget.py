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
    
    print(f'Using API key: {api_key[:5]}...')
    print(f'Using sub-account: {sub_account}')
    
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
            formatted_position = {
                'has_position': True,
                'position_side': position.get('side', '').lower(),
                'entry_price': float(position.get('entryPrice', 0)),
                'current_price': float(position.get('markPrice', 0)) if position.get('markPrice') else 0,
                'position_size': float(position.get('contracts', 0)),
                'leverage': int(position.get('leverage', 1)),
                'risk_multiplier': 1.0,  # Default
                'pnl_percent': float(position.get('percentage', 0)) if position.get('percentage') else 0,
                'pnl_usd': float(position.get('unrealizedPnl', 0)) if position.get('unrealizedPnl') else 0,
                'stop_loss': float(position.get('stopLossPrice', 0)) if position.get('stopLossPrice') else 0,
                'entry_time': position.get('timestamp', ''),
                'source': 'bitget',
                'timestamp': position.get('timestamp', '')
            }
            
            # Store in Redis
            r.set('current_position', json.dumps(formatted_position))
            print(f'Stored position data in Redis')
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