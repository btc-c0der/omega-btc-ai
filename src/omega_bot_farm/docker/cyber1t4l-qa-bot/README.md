
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


# CyBer1t4L QA Bot - Docker Setup

The CyBer1t4L QA Bot is an advanced quality assurance system for the OMEGA Trading Ecosystem. It monitors test coverage, performs real-time QA, and maintains the sacred harmony of the codebase.

## 🧬 Features

- Comprehensive test coverage analysis
- Real-time monitoring of critical systems
- Automated test generation for low-coverage code
- Discord integration for QA reporting
- Kubernetes-ready deployment

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- A Discord server where you have admin privileges
- Discord bot credentials (Application ID, Public Key, and Bot Token)

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/your-username/omega-btc-ai.git
cd omega-btc-ai
```

2. **Configure environment variables**

Create a `.env` file in the project root or ensure these variables are in your environment:

```
CYBER1T4L_APP_ID=your_application_id
CYBER1T4L_PUBLIC_KEY=your_public_key
DISCORD_BOT_TOKEN=your_bot_token
```

3. **Build and run with Docker Compose**

```bash
cd src/omega_bot_farm/docker/cyber1t4l-qa-bot
docker-compose up -d
```

## 🤖 Adding the Bot to Discord

1. Use the following URL template to add the bot to your Discord server:

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_APP_ID&permissions=274878221376&scope=bot%20applications.commands
```

2. Replace `YOUR_APP_ID` with your `CYBER1T4L_APP_ID` value
3. Open the URL in your browser
4. Select your Discord server and click "Authorize"
5. Complete any verification steps

The permissions included are:

- Read messages/view channels
- Send messages
- Embed links
- Attach files
- Use slash commands
- Use application commands

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_HOST` | Redis server hostname | `redis` |
| `REDIS_PORT` | Redis server port | `6379` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `CYBER1T4L_APP_ID` | Discord application ID | (required) |
| `CYBER1T4L_PUBLIC_KEY` | Discord public key | (required) |
| `DISCORD_BOT_TOKEN` | Discord bot token | (required) |
| `COVERAGE_THRESHOLD` | Minimum acceptable test coverage | `80.0` |
| `TESTING_INTERVAL_MINUTES` | How often to run tests | `60` |

## 📊 Bot Commands

When added to your Discord server, CyBer1t4L supports the following commands:

- `/coverage` - Get the current test coverage report
- `/test [module]` - Run tests for a specific module
- `/monitor` - Start real-time monitoring
- `/qa_status` - Get the overall QA status of the codebase

## 🔄 Kubernetes Deployment

The CyBer1t4L QA Bot is designed to run in a Kubernetes cluster. To deploy it:

1. Ensure your Kubernetes cluster is up and running
2. Apply the Kubernetes configuration:

```bash
kubectl apply -f src/omega_bot_farm/kubernetes/deployments/cyber1t4l-qa-bot.yaml
```

## 🔒 Security Considerations

- The bot requires Discord credentials which should be kept secure
- The credentials are stored in Kubernetes secrets in the cluster
- For local development, use `.env` files which are not committed to the repository
- The bot requires read access to the codebase to perform coverage analysis

## 📚 Documentation

For more information on how the CyBer1t4L QA Bot works, see:

- [API Documentation](../../API.md)
- [Architecture Documentation](../../ARCHITECTURE.md)
- [Installation Guide](../../INSTALLATION.md)

## 🧪 Testing

To test the Docker image locally:

```bash
# Build the image
docker build -t omega-btc-ai/cyber1t4l-qa-bot:latest -f Dockerfile ../../..

# Run with required environment variables
docker run -it --rm \
  -e CYBER1T4L_APP_ID=your_app_id \
  -e CYBER1T4L_PUBLIC_KEY=your_public_key \
  -e DISCORD_BOT_TOKEN=your_bot_token \
  omega-btc-ai/cyber1t4l-qa-bot:latest
```
