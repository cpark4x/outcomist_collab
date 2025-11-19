.PHONY: help install dev build up down logs clean test format

help:
	@echo "Outcomist - Development Commands"
	@echo "================================"
	@echo ""
	@echo "Docker commands:"
	@echo "  make build      - Build Docker images"
	@echo "  make up         - Start services"
	@echo "  make down       - Stop services"
	@echo "  make logs       - View logs"
	@echo "  make restart    - Restart services"
	@echo "  make clean      - Remove containers and volumes"
	@echo ""
	@echo "Development commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make dev        - Run development servers"
	@echo "  make test       - Run tests"
	@echo "  make format     - Format code"
	@echo ""
	@echo "Utility commands:"
	@echo "  make backup     - Backup data directory"
	@echo "  make health     - Check service health"

# Docker commands
build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✅ Services started"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend:  http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose restart

clean:
	docker-compose down -v
	@echo "⚠️  All containers and volumes removed"

# Development commands
install:
	@echo "Installing backend dependencies..."
	cd backend && python -m venv .venv && .venv/bin/pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ Dependencies installed"

dev:
	@echo "Starting development servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@echo ""
	@echo "Run in separate terminals:"
	@echo "  Terminal 1: cd backend && source .venv/bin/activate && uvicorn src.main:app --reload"
	@echo "  Terminal 2: cd frontend && npm run dev"

test:
	@echo "Running backend tests..."
	cd backend && .venv/bin/pytest
	@echo "Running frontend tests..."
	cd frontend && npm test

format:
	@echo "Formatting backend..."
	cd backend && .venv/bin/black src/ && .venv/bin/isort src/
	@echo "Formatting frontend..."
	cd frontend && npm run format
	@echo "✅ Code formatted"

# Utility commands
backup:
	@mkdir -p backups
	@BACKUP_FILE="backups/webapp-backup-$$(date +%Y%m%d-%H%M%S).tar.gz"
	@tar -czf $$BACKUP_FILE data/
	@echo "✅ Backup created: $$BACKUP_FILE"

health:
	@echo "Checking backend..."
	@curl -s http://localhost:8000/health | python -m json.tool
	@echo ""
	@echo "Checking frontend..."
	@curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:3000/
