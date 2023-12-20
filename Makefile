.PHONY: lint
lint: ## Run linters
	isort .
	mypy .


.PHONY: run-dev
run-dev: ## Run backend on development
	uvicorn run:app --port 8500 --reload 

	
.PHONY: run-prod
run-prod: ## Run backend on production
	gunicorn run:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:6666


.PHONY: migrate-up
migrate-up: ## Run migrations
	alembic revision --autogenerate -m "never" && alembic upgrade head

.PHONY: docker-run
docker-run:
	docker-compose -f docker/docker-compose.yml up -d

.PHONY: kafka-Run
kafka-run: ## Run Kafka 
	faust -A pkg.main worker -l info