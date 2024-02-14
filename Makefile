SERVER_IMAGE = ephemeralchat_server:latest
PROXY_IMAGE = envoy_proxy:latest

.PHONY: build_server run_backend stop_backend

build_server:
	docker build -t $(SERVER_IMAGE) ./server

run_backend:
	docker-compose up -d

stop_backend:
	docker-compose down

help:
	@echo "Available targets:"
	@echo "  build_server   - Build the server Docker image"
	@echo "  run_backend    - Run the backend Docker containers"
	@echo "  stop_backend   - Stop the backend Docker containers"