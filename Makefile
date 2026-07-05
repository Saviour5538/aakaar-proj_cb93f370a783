# Makefile for managing the DocMind project

.PHONY: install dev build test docker-up docker-down clean

install:
	# Install backend dependencies
	pip install -r backend/requirements.txt
	# Install frontend dependencies
	cd frontend && npm install

dev:
	# Start the development environment
	./scripts/dev.sh

build:
	# Build the frontend for production
	cd frontend && npm run build

test:
	# Run backend tests
	pytest
	# Run frontend tests
	cd frontend && npm test

docker-up:
	# Start all services using Docker Compose
	docker-compose up --build -d

docker-down:
	# Stop all services and remove containers
	docker-compose down

clean:
	# Remove all build artifacts and temporary files
	rm -rf backend/__pycache__
	rm -rf frontend/node_modules
	rm -rf frontend/dist
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage