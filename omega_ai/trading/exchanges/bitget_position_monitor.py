"""
BitGet Position Monitor

This module implements position monitoring and exit strategy execution
for BitGet exchange positions.

Copyright (c) 2024 OMEGA BTC AI
Licensed under the GBU2 License - see LICENSE file for details
"""

async def monitor_bitget_positions(trader, exit_strategy):
    """Monitor BitGet positions and apply exit strategy"""
    running = True
    while running:
        try:
            # Get current positions
            positions = await trader.get_positions()
            
            # For each active position
            for position in positions:
                position_id = position.get('id', '')
                symbol = position.get('symbol', '')
                contracts = float(position.get('contracts', 0))
                entry_price = float(position.get('entryPrice', 0))
                current_price = float(position.get('markPrice', 0))
                direction = position.get('side', '').lower()
                
                if contracts <= 0 or entry_price <= 0 or current_price <= 0:
                    continue
                
                # Get latest trap data
                trap_data = await get_latest_trap_data()
                
                # Update trailing stops
                new_stop = await exit_strategy.update_trailing_stops(position_id, current_price)
                if new_stop and new_stop != position.get('stopLossPrice'):
                    await update_stop_loss_order(trader, position, new_stop)
                
                # Check for exit conditions
                should_exit, exit_info = await exit_strategy.check_for_exit(
                    position_id, current_price, trap_data
                )
                
                if should_exit:
                    # Execute the exit
                    exit_percentage = exit_info.get('percentage', 100)
                    exit_price = exit_info.get('price', current_price)
                    reason = exit_info.get('reason', 'unknown')
                    
                    # Log the exit
                    logger.info(f"Exit signal for {symbol} {direction} position: "
                               f"{exit_percentage}% at {exit_price} due to {reason}")
                    
                    try:
                        # Execute partial or full close
                        size_to_close = contracts * (exit_percentage / 100)
                        await trader.close_position(symbol, size_to_close, direction)
                        
                        # Update tracking
                        await exit_strategy.process_partial_exit(position_id, exit_info)
                        logger.info(f"Successfully closed {exit_percentage}% of {symbol} position")
                    except Exception as e:
                        # If API fails, try alternative closing method
                        logger.error(f"Error closing position: {e}")
                        await try_alternative_closing_method(trader, position, exit_percentage)
            
            # Sleep to prevent API rate limiting
            await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"Error in position monitor: {e}")
            await asyncio.sleep(30)  # Longer sleep on error
