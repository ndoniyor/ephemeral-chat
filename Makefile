SERVER_IMAGE = ephemeralchat_server:latest
PROXY_IMAGE = envoy_proxy:latest

.PHONY: flush_server python_proto build_server run_backend stop_backend

flush_server:
	@curl --silent --output /dev/null --location 'http://localhost:8080/grpc.Chat/FlushServer' \
	--header 'Accept: application/grpc-web-text' \
	--header 'Referer: http://localhost:5173/' \
	--header 'content-type: application/grpc-web-text' \
	--header 'x-grpc-web: 1' \
	--header 'Origin: http://localhost:5173' \
	--data 'AAAAAAA='

python_proto:
	./server/virtualenv/bin/python3 -m grpc_tools.protoc -I ./ --python_out=./server/servicer --grpc_python_out=./server/servicer ./protos/chat.proto

build_server:
	docker build -t $(SERVER_IMAGE) ./server

start_backend:
	docker-compose up -d

stop_backend:
	docker-compose down

help:
	@echo "Available targets:"
	@echo "  flush_server   - Flush the server's conversations"
	@echo "  python_proto   - Generate Python code from the proto file"
	@echo "  build_server   - Build the server Docker image"
	@echo "  start_backend    - Run the backend Docker containers"
	@echo "  stop_backend   - Stop the backend Docker containers"
