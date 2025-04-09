# 🔱 OMEGA BTC AI - SACRED MAKEFILE 🔱

.PHONY: install start stop restart clean monitor stats tree

# Divine Variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Divine Installation
install:
	@echo "🧪 Installing divine dependencies..."
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	@echo "✨ Divine installation complete!"

# Divine Environment Setup
setup:
	@echo "🔧 Setting up divine environment..."
	mkdir -p tests/{matrix,prophecy,core,utils}
	mkdir -p .tmuxinator
	@echo "✨ Divine environment ready!"

# Divine Test Listener
start:
	@echo "🚀 Starting divine test listener..."
	tmuxinator start neo-matrix-test

stop:
	@echo "🛑 Stopping divine test listener..."
	tmuxinator stop neo-matrix-test

restart:
	@echo "🔄 Restarting divine test listener..."
	tmuxinator restart neo-matrix-test

# Divine Monitoring
monitor:
	@echo "📊 Starting divine monitoring stack..."
	docker-compose -f orchestrator/docker-compose.monitoring.yml up -d

monitor-stop:
	@echo "🛑 Stopping divine monitoring stack..."
	docker-compose -f orchestrator/docker-compose.monitoring.yml down

# Divine Test Statistics
stats:
	@echo "📈 Showing divine test statistics..."
	$(PYTHON) omega-test-listener.py stats

tree:
	@echo "🌳 Showing divine test tree..."
	$(PYTHON) omega-test-listener.py tree

# Divine Cleanup
clean:
	@echo "🧹 Cleaning divine environment..."
	rm -rf $(VENV)
	rm -f test_results.db
	rm -f divine_test_listener.log
	docker-compose -f orchestrator/docker-compose.monitoring.yml down -v
	@echo "✨ Divine cleanup complete!"

# Divine Help
help:
	@echo "🔱 OMEGA BTC AI - Divine Test Listener"
	@echo ""
	@echo "Available commands:"
	@echo "  make install     - Install divine dependencies"
	@echo "  make setup      - Set up divine environment"
	@echo "  make start      - Start divine test listener"
	@echo "  make stop       - Stop divine test listener"
	@echo "  make restart    - Restart divine test listener"
	@echo "  make monitor    - Start divine monitoring stack"
	@echo "  make monitor-stop - Stop divine monitoring stack"
	@echo "  make stats      - Show divine test statistics"
	@echo "  make tree       - Show divine test tree"
	@echo "  make clean      - Clean divine environment"
	@echo "  make help       - Show this help message" 