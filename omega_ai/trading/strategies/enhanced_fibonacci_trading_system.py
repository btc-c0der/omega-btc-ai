class EnhancedFibonacciTradingSystem:
    """Main system integrating all components for enhanced Fibonacci trading."""
    
    def __init__(self, api_key=None, api_secret=None, passphrase=None, 
                sub_account=None, use_testnet=False):
        """Initialize the enhanced Fibonacci trading system."""
        # Setup Redis client
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        
        # Initialize trader
        self.trader = BitGetCCXT(
            api_key=api_key, 
            api_secret=api_secret, 
            password=passphrase,
            use_testnet=use_testnet,
            sub_account=sub_account
        )
        
        # Initialize exit manager
        self.exit_manager = EnhancedFibonacciExitManager(
            redis_client=self.redis_client,
            base_risk_percent=1.0,
            tp_layers=4,
            sl_multiplier=1.0,
            enable_trailing=True,
            trailing_activation_pct=1.0,
            risk_reward_ratio=2.5,
            scalper_coefficient=0.3,
            aggressive_coefficient=0.1,
            trap_sensitivity=0.7
        )
        
        # Initialize position monitor
        self.position_monitor = BitGetPositionMonitor(
            trader=self.trader,
            exit_manager=self.exit_manager,
            polling_interval=5
        )
        
        # Initialize profile balancer
        self.profile_balancer = ProfileBalancer(
            redis_client=self.redis_client,
            initial_scalper_coef=0.3,
            initial_strategic_coef=0.6,
            initial_aggressive_coef=0.1
        )
        
        # Logger setup
        self.logger = logging.getLogger('fibonacci_trading_system')
        
        # Tasks
        self.tasks = []
        self.running = False
    
    async def initialize(self):
        """Initialize all components."""
        await self.trader.initialize()
        self.logger.info("Trader initialized")
    
    async def start(self):
        """Start the trading system."""
        self.running = True
        
        # Start position monitoring
        await self.position_monitor.start_monitoring()
        
        # Start database updates
        db_task = asyncio.create_task(self._update_database())
        self.tasks.append(db_task)
        
        self.logger.info("Enhanced Fibonacci Trading System started")
    
    async def stop(self):
        """Stop the trading system."""
        self.running = False
        
        # Stop position monitoring
        await self.position_monitor.stop_monitoring()
        
        # Cancel all tasks
        for task in self.tasks:
            task.cancel()
        
        # Close trader connection
        await self.trader.close()
        
        self.logger.info("Enhanced Fibonacci Trading System stopped")
    
    async def _update_database(self):
        """Update trading metrics in the database."""
        while self.running:
            try:
                # Get current positions
                positions = await self.trader.get_positions()
                
                # Update positions in Redis
                self.redis_client.set('current_positions', json.dumps(positions))
                
                # Get current balance
                balance = await self.trader.get_balance()
                
                # Update balance in Redis
                self.redis_client.set('current_balance', json.dumps(balance))
                
                # Sleep before next update
                await asyncio.sleep(30)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error updating database: {e}")
                await asyncio.sleep(60)