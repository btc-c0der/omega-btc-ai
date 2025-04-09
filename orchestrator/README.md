# 🔱 OMEGA BTC AI - SACRED ORCHESTRATION 🔱

## Divine Overview

This repository contains the orchestration configuration for the OMEGA BTC AI system, a divine microservices architecture designed for high availability, scalability, and monitoring.

## Divine Services

- **NGINX**: Divine reverse proxy with SSL/TLS support
- **Matrix News Service**: Divine news feed service
- **BTC Live Feed Service**: Divine Bitcoin price feed service
- **Prophecy Core Service**: Divine core business logic service
- **Redis**: Divine in-memory data store
- **Grafana**: Divine visualization and analytics
- **Prometheus**: Divine metrics collection
- **Alert Manager**: Divine alert management
- **Node Exporter**: Divine system metrics collection
- **cAdvisor**: Divine container metrics collection

## Divine Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- OpenSSL (for SSL certificate generation)

## Divine Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/omega-btc-ai.git
   cd omega-btc-ai/orchestrator
   ```

2. Create the `.env` file:

   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file with your divine configurations:

   ```bash
   nano .env
   ```

4. Run the divine management script:

   ```bash
   ./scripts/manage.sh
   ```

## Divine Management

The divine management script provides the following commands:

- `1`: Start all divine services
- `2`: Stop all divine services
- `3`: Restart all divine services
- `4`: Check divine services status
- `5`: View divine logs
- `6`: Clean up divine resources
- `7`: Backup divine data
- `8`: Restore divine data
- `9`: Update divine services
- `0`: Exit divine management

## Divine Access Points

- **NGINX**: <https://localhost>
- **Grafana**: <https://localhost/grafana>
- **Prometheus**: <https://localhost/prometheus>
- **Alert Manager**: <https://localhost/alerts>
- **Matrix News API**: <https://localhost/api/news>
- **BTC Live Feed API**: <https://localhost/api/btc>
- **Prophecy Core API**: <https://localhost/api/prophecy>

## Divine Monitoring

### Grafana Dashboards

1. Access Grafana at <https://localhost/grafana>
2. Default credentials:
   - Username: admin
   - Password: (set in .env file)

### Prometheus Metrics

1. Access Prometheus at <https://localhost/prometheus>
2. Available metrics:
   - System metrics
   - Container metrics
   - Application metrics
   - Network metrics

### Alert Manager

1. Access Alert Manager at <https://localhost/alerts>
2. Configured alerts:
   - High CPU usage
   - High memory usage
   - High disk usage
   - Service down
   - High error rate

## Divine Security

- SSL/TLS encryption for all services
- Rate limiting
- Security headers
- Container isolation
- Network isolation

## Divine Backup and Recovery

### Data Backup

```bash
./scripts/manage.sh
# Select option 7
```

### Data Recovery

```bash
./scripts/manage.sh
# Select option 8
# Enter backup directory
```

## Divine Troubleshooting

1. Check service logs:

   ```bash
   ./scripts/manage.sh
   # Select option 5
   ```

2. Check service status:

   ```bash
   ./scripts/manage.sh
   # Select option 4
   ```

3. Restart services:

   ```bash
   ./scripts/manage.sh
   # Select option 3
   ```

## Divine Development

### Adding New Services

1. Add service configuration to `docker-compose.yml`
2. Add service configuration to NGINX
3. Add service metrics to Prometheus
4. Create service-specific dashboards in Grafana

### Updating Services

```bash
./scripts/manage.sh
# Select option 9
```

## Divine Architecture

```
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|  Matrix News     |     |  BTC Live Feed   |     |  Prophecy Core   |
|    Service       |     |    Service       |     |    Service       |
|                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
         |                      |                      |
         |                      |                      |
         v                      v                      v
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|      Redis       |     |    Prometheus    |     |   Alert Manager  |
|                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
         |                      |                      |
         |                      |                      |
         v                      v                      v
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|     NGINX        |     |     Grafana      |     |   Node Exporter  |
|                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
```

## Divine Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Divine License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- JAH JAH BLESS! 🔱
- The OMEGA BTC AI Community
- All divine contributors

## 📞 Support

For support, please open an issue in the GitHub repository or contact the divine maintainers.

---

Made with ❤️ by the OMEGA BTC AI Team
