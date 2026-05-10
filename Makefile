# Eko AI Business Automation — Operations Makefile
# Usage: make <target>

.PHONY: help up down restart build test logs db-shell backup lint

help: ## Show this help message
	@echo "Eko AI Operations"
	@echo "================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Start all services (production mode)
	docker compose up -d

dev: ## Start backend + frontend dev server with HMR
	docker compose up -d backend redis db
	docker compose --profile dev up -d frontend-dev

down: ## Stop all services
	docker compose down

restart: down up ## Restart all services

build: ## Rebuild all containers
	docker compose build --no-cache

test: ## Run backend tests (requires services running)
	cd backend && pytest tests/ -v --tb=short

lint: ## Run ruff linter on backend
	cd backend && ruff check app/ || true

logs: ## Tail backend logs
	docker logs -f eko-backend --tail 50

logs-worker: ## Tail celery worker logs
	docker logs -f eko-ai-bussinnes-automation-celery-worker-1 --tail 50

logs-beat: ## Tail celery beat logs
	docker logs -f eko-celery-beat --tail 20

db-shell: ## Open PostgreSQL shell
	docker exec -it eko-db psql -U eko -d eko_ai

db-backup: ## Backup database to ./backups/
	@mkdir -p backups
	docker exec eko-db pg_dump -U eko eko_ai > backups/eko_ai_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Backup saved to backups/"

backup-leads: ## Export processed leads to JSON
	docker exec eko-backend python3 -c "import asyncio; from app.tasks.scheduled import backup_processed_leads; print(asyncio.run(backup_processed_leads()))"

health: ## Check backend health
	@curl -s http://localhost:8000/health | python3 -m json.tool || echo "Backend not responding"

clean: ## Remove unused Docker images and volumes
	docker system prune -f
	docker volume prune -f

frontend-build: ## Build frontend for production
	cd frontend && npm ci && npm run build
