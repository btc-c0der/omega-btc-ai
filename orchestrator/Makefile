# 🔱 OMEGA BTC AI - Divine Orchestrator Makefile 🔱

.PHONY: up down rebuild logs ps clean bless

# Divine Variables
COMPOSE_FILE=docker-compose.yml
NETWORK_NAME=omega_btc_network

# 🌟 Core Commands
up:
	@echo "🔱 Raising the Divine Services..."
	docker-compose -f $(COMPOSE_FILE) up -d
	@echo "✨ Services are now blessed and running"

down:
	@echo "🌙 Bringing down the Divine Services..."
	docker-compose -f $(COMPOSE_FILE) down
	@echo "💫 Services have returned to the cosmic void"

rebuild:
	@echo "🔄 Rebuilding the Divine Containers..."
	docker-compose -f $(COMPOSE_FILE) build --no-cache
	@echo "✨ Containers have been reborn"

logs:
	@echo "📜 Reading the Divine Logs..."
	docker-compose -f $(COMPOSE_FILE) logs -f

ps:
	@echo "👁️ Viewing the Divine Services..."
	docker-compose -f $(COMPOSE_FILE) ps

clean:
	@echo "🧹 Cleansing the Divine Environment..."
	docker-compose -f $(COMPOSE_FILE) down -v
	docker system prune -f
	@echo "✨ Environment is now pure"

bless:
	@echo "🙏 Blessing the Divine Services..."
	@for service in $$(docker-compose -f $(COMPOSE_FILE) ps --services); do \
		echo "✨ Blessing $$service..."; \
		docker-compose -f $(COMPOSE_FILE) restart $$service; \
	done
	@echo "🌟 All services have been blessed"

# 🔮 Development Commands
dev:
	@echo "🧪 Starting Divine Development Environment..."
	docker-compose -f $(COMPOSE_FILE) -f docker-compose.dev.yml up -d

test:
	@echo "🧪 Running Divine Tests..."
	docker-compose -f $(COMPOSE_FILE) run --rm test-runner pytest

# 🌌 Monitoring Commands
monitor:
	@echo "🔍 Activating Divine Monitoring..."
	docker-compose -f $(COMPOSE_FILE) -f docker-compose.monitoring.yml up -d

# 🛡️ Security Commands
secure:
	@echo "🛡️ Strengthening Divine Security..."
	docker-compose -f $(COMPOSE_FILE) -f docker-compose.security.yml up -d

# 📊 Backup Commands
backup:
	@echo "💾 Creating Divine Backup..."
	./scripts/create_state_snapshot.sh

restore:
	@echo "🔄 Restoring Divine State..."
	./scripts/restore_state_snapshot.sh

# 🌟 Help Command
help:
	@echo "🔱 OMEGA BTC AI - Divine Orchestrator Commands 🔱"
	@echo ""
	@echo "Core Commands:"
	@echo "  make up      - Raise all divine services"
	@echo "  make down    - Return services to the void"
	@echo "  make rebuild - Rebuild divine containers"
	@echo "  make logs    - View divine logs"
	@echo "  make ps      - List divine services"
	@echo "  make clean   - Cleanse the environment"
	@echo "  make bless   - Bless all services"
	@echo ""
	@echo "Development:"
	@echo "  make dev     - Start development environment"
	@echo "  make test    - Run divine tests"
	@echo ""
	@echo "Monitoring:"
	@echo "  make monitor - Activate divine monitoring"
	@echo ""
	@echo "Security:"
	@echo "  make secure  - Strengthen divine security"
	@echo ""
	@echo "Backup:"
	@echo "  make backup  - Create divine backup"
	@echo "  make restore - Restore divine state"
	@echo ""
	@echo "JAH JAH BLESS! 🔱" 