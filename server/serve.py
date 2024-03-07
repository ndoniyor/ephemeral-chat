import logging
from concurrent.futures import ThreadPoolExecutor
import grpc

import grpc_services.generated_protos.chat_service_pb2_grpc as chat_service_grpc
from grpc_services.server import Server

ADDRESS = "localhost"
PORT = 11912


def serve():
    logging.basicConfig(level=logging.INFO)

    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    chat_service_grpc.add_ChatServicer_to_server(Server(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()

    logging.info(f"Listening on {ADDRESS}:{PORT}...")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
