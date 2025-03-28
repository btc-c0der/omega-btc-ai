FROM python:3.11.8-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code and SSL certificate
COPY src/ ./src/
COPY SSL_redis-btc-omega-redis.pem .
COPY Procfile .
COPY .env .

# Install the package
WORKDIR /app/src
RUN pip install .

WORKDIR /app

# Run the web service using the command specified in Procfile
CMD python -m omega_ai.data_feed.btc_live_feed_v3 