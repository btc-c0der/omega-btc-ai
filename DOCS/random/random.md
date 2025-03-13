🔥 JAH BLESS! SETTING UP THE OMEGA DATABASE & COMMAND SEQUENCE! 🔱🚀
💡 Before running the full MM trap detection system, we must ensure the database is running & accessible.The steps below will:✅ Start the database✅ Test the DB connection✅ Provide the full sequence of commands to execute OMEGA AI BTC from scratch

📌 Step 1: Start the Database
If you're using SQLite (default for OMEGA AI BTC), no separate database service is required.If you're using PostgreSQL or MySQL, follow the commands below.
Option 1️⃣: SQLite (Default)
No extra setup needed! The DB is created automatically inside data/mm_traps.db.Run:
python omega_ai/db_manager/database.py
Expected Output:
✅ Database initialized and ready for MM trap logging!

Option 2️⃣: PostgreSQL (Advanced)
1️⃣ Start PostgreSQL (If not already running)
sudo systemctl start postgresql  # Linux
brew services start postgresql   # macOS (Homebrew)
2️⃣ Connect to PostgreSQL
psql -U omega_user -d omega_db
3️⃣ Manually Test DB
SELECT * FROM mm_traps LIMIT 5;
Expected Output:
 id | timestamp  | btc_price | change  | trap_type 
----+-----------+-----------+---------+-----------
  1 | 2025-03-07T15:45:10Z | 90235.45 | -2.45% | Fakeout
(1 row)

📌 Step 2: Verify DB Connection
Run this Python script to confirm DB connectivity:
from omega_ai.db_manager.database import setup_database, test_connection

setup_database()
test_connection()
Expected Output:
✅ Database initialized!
✅ Connection successful!

📌 Full Sequence: Running OMEGA AI BTC from Scratch
1️⃣ Start Database (if needed)
python omega_ai/db_manager/database.py
2️⃣ Start BTC Live Feed
python omega_ai/data_feed/btc_live_feed.py
3️⃣ Run MM Trap Detector
python omega_ai/mm_trap_detector/mm_trap_analyzer.py
4️⃣ (Optional) Run AI Predictions
python omega_ai/ai_models/btc_prediction.py

📌 One-Line Script to Start Everything
Want to run everything at once? Create start_omega.sh in the root folder:
#!/bin/bash
echo "🚀 Starting OMEGA AI BTC System..."
python omega_ai/db_manager/database.py &
sleep 2
python omega_ai/data_feed/btc_live_feed.py &
sleep 2
python omega_ai/mm_trap_detector/mm_trap_analyzer.py &
sleep 2
echo "✅ OMEGA AI BTC System is Live!"
Run it:
chmod +x start_omega.sh
./start_omega.sh

📌 Expected Final Output (LIVE)
✅ Database initialized and ready for MM trap logging!
✅ Connected to Binance WebSocket - Listening for BTC price updates...
📡 LIVE BTC PRICE UPDATE: $90235.45
📡 LIVE BTC PRICE UPDATE: $90237.80
⚠️ LIQUIDITY GRAB DETECTED! BTC moved -$1200 with Schumann at 10.75 Hz!
📡 LIVE BTC PRICE UPDATE: $90500.78
⚠️ FAKE PUMP DETECTED! BTC jumped +6.02% rapidly!
📡 LIVE BTC PRICE UPDATE: $90010.32
⚠️ MM ACCUMULATION DETECTED! BTC stabilizing within ±$200 with Schumann at 9.15 Hz!

🔥 NEXT STEPS
✅ Verify Database Setup & Connection✅ Run the full system from scratch✅ Confirm BTC price updates & MM traps detected live✅ Test AI predictions for MM movements
🔥 THE OMEGA GRID IS FULLY OPERATIONAL! 🔱🚀Let me know if you need any adjustments! 💛💚❤️
