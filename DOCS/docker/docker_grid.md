
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


🔥 **OMEGA GRID - FULL DOCKER SETUP** 🚀💥  
**We’re going to containerize the entire project: Redis, PostgreSQL, WebSockets, BTC AI, and Grafana!**  

### **1️⃣ Folder Structure for Dockerized OMEGA GRID**
Ensure your **project folder** has this structure:

```
omega_grid/
│── docker-compose.yml      # ✅ The core of the deployment
│── Dockerfile              # ✅ The main app Dockerfile
│── .env                    # ✅ Environment variables
│── omega_ai/               # ✅ The main Python app
│── db/                     # ✅ Database initialization
│   ├── init.sql            # ✅ PostgreSQL setup script
│── redis/                  # ✅ Redis configuration
│── grafana/                # ✅ Grafana dashboards & config
│── websocket/              # ✅ WebSocket services
│── btc_live_feed/          # ✅ BTC data ingestion
│── visualization/          # ✅ Grafana + Dash dashboard
│── requirements.txt        # ✅ Python dependencies
```

---

### **2️⃣ Create `docker-compose.yml` (Master Setup)**
This will spin up:
✅ **PostgreSQL** (DB)  
✅ **Redis** (Caching + Queue)  
✅ **WebSockets** (Live BTC data)  
✅ **BTC AI Engine** (Trap Detector)  
✅ **Grafana** (Monitoring)  

📄 **Create `docker-compose.yml` in the project root:**
```yaml
version: '3.8'

services:
  # ✅ PostgreSQL Database
  postgres:
    image: postgres:15
    container_name: omega_db
    restart: always
    environment:
      POSTGRES_DB: omega_db
      POSTGRES_USER: omega_user
      POSTGRES_PASSWORD: omega_pass
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql

  # ✅ Redis (Message Queue & Caching)
  redis:
    image: redis:latest
    container_name: omega_redis
    restart: always
    ports:
      - "6379:6379"
    command: redis-server --save 20 1 --loglevel warning
    volumes:
      - redis_data:/data

  # ✅ WebSocket Server for BTC Data
  mm_websocket:
    build: ./websocket
    container_name: omega_mm_websocket
    restart: always
    depends_on:
      - redis
    ports:
      - "8765:8765"

  # ✅ BTC Live Data Feed
  btc_live_feed:
    build: ./btc_live_feed
    container_name: omega_btc_feed
    restart: always
    depends_on:
      - redis
    environment:
      REDIS_HOST: redis
      REDIS_PORT: 6379

  # ✅ OMEGA BTC AI (Market Maker Trap Detector)
  omega_ai:
    build: ./omega_ai
    container_name: omega_ai
    restart: always
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://omega_user:omega_pass@postgres:5432/omega_db
      REDIS_HOST: redis
      REDIS_PORT: 6379

  # ✅ Grafana for Monitoring
  grafana:
    image: grafana/grafana:latest
    container_name: omega_grafana
    restart: always
    depends_on:
      - redis
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning

volumes:
  pg_data:
  redis_data:
  grafana_data:
```

---

### **3️⃣ Create `Dockerfile` for Python Services**
📄 **Create `Dockerfile` in `omega_ai/`, `btc_live_feed/`, and `websocket/`**
```dockerfile
# Base Image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "main.py"]
```

---

### **4️⃣ Initialize PostgreSQL DB**
📄 **Create `db/init.sql`**
```sql
CREATE TABLE IF NOT EXISTS btc_prices (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    btc_price DECIMAL(18,8),
    volume DECIMAL(18,8)
);

CREATE TABLE IF NOT EXISTS subtle_movements (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    btc_price DECIMAL(18,8),
    prev_price DECIMAL(18,8),
    absolute_change DECIMAL(18,8),
    price_change_percentage DECIMAL(18,8),
    movement_tag TEXT,
    volume DECIMAL(18,8)
);
```

---

### **5️⃣ Build & Run Everything**
🚀 **To start all services, run:**  
```bash
docker-compose up --build -d
```
🔥 **To check running containers:**  
```bash
docker ps
```
🛠 **To stop services:**  
```bash
docker-compose down
```

---

### **6️⃣ Verify Services**
✅ **Grafana** → Open **http://localhost:3000**  
✅ **WebSockets** → Listening on **ws://localhost:8765**  
✅ **Redis** → Use `redis-cli` to check data  
✅ **Postgres** → Connect via `psql`  

---

🔥 **NOW THE OMEGA GRID IS 100% DOCKERIZED & READY FOR DEPLOYMENT!** 🚀  
💛 **JAH BLESS THE OMEGA REVOLUTION!** 💚❤️