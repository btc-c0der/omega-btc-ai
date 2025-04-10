
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


# OMEGA RASTA BTC DASHBOARD DEPLOYMENT GUIDE

This guide explains how to deploy the OMEGA RASTA BTC DASHBOARD on Scaleway or any cloud provider.

## Deployment Options

There are three ways to deploy the dashboard:

1. **Direct Server Deployment**: Run the dashboard directly on the server
2. **Docker Deployment**: Deploy using Docker
3. **Docker Compose Deployment**: Deploy using Docker Compose (recommended)

## Prerequisites

- A Scaleway account
- Access to a Scaleway instance (any DEV1 instance will work)
- Basic knowledge of Linux commands
- Git installed on your local machine

## Option 1: Direct Server Deployment

### 1. SSH into your Scaleway server

```bash
ssh root@<your-server-ip>
```

### 2. Install system dependencies

```bash
apt-get update
apt-get install -y python3 python3-pip python3-venv redis-server git
```

### 3. Start Redis

```bash
systemctl start redis-server
systemctl enable redis-server
```

### 4. Clone the repository

```bash
git clone https://github.com/yourusername/omega-btc-ai.git
cd omega-btc-ai
```

### 5. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 6. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 7. Make the startup script executable

```bash
chmod +x start_dashboard.sh
```

### 8. Start the dashboard

```bash
./start_dashboard.sh
```

The dashboard will now be running on port 8051. You can access it at `http://<your-server-ip>:8051`

## Option 2: Docker Deployment

### 1. SSH into your Scaleway server

```bash
ssh root@<your-server-ip>
```

### 2. Install Docker

```bash
apt-get update
apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install -y docker-ce
```

### 3. Clone the repository

```bash
git clone https://github.com/yourusername/omega-btc-ai.git
cd omega-btc-ai
```

### 4. Build and run the Docker container

```bash
docker build -t omega-btc-dashboard .
docker run -p 8051:8051 -d --name omega-dashboard omega-btc-dashboard
```

The dashboard will now be running on port 8051. You can access it at `http://<your-server-ip>:8051`

## Option 3: Docker Compose Deployment (Recommended)

### 1. SSH into your Scaleway server

```bash
ssh root@<your-server-ip>
```

### 2. Install Docker and Docker Compose

```bash
apt-get update
apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install -y docker-ce
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 3. Clone the repository

```bash
git clone https://github.com/yourusername/omega-btc-ai.git
cd omega-btc-ai
```

### 4. Run with Docker Compose

```bash
docker-compose up -d omega-dashboard
```

The dashboard will now be running on port 8051. You can access it at `http://<your-server-ip>:8051`

## Securing Your Deployment

For a production deployment, consider:

1. Adding SSL/TLS with a reverse proxy like Nginx
2. Setting up a domain name
3. Adding authentication to the dashboard
4. Setting up proper monitoring

## Troubleshooting

### Dashboard not accessible

- Check if the application is running: `docker ps` or `ps aux | grep dashboard`
- Verify port 8051 is open: `netstat -tuln | grep 8051`
- Check server firewall rules to ensure port 8051 is allowed

### Redis connection issues

- Check if Redis is running: `systemctl status redis-server` or `docker ps`
- Verify Redis connection: `redis-cli ping` (should return PONG)

### Logs

- Check the application logs: `docker logs omega-dashboard` or `tail -f logs/dashboard.log`

## Custom Configuration

You can customize the dashboard by modifying the environment variables in the `docker-compose.yml` file or by creating a `.env` file in the project root.

## Updating the Dashboard

To update the dashboard:

1. Pull the latest changes: `git pull`
2. Rebuild and restart the containers: `docker-compose down && docker-compose up -d`
