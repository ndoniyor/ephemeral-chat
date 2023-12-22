import logging
from concurrent.futures import ThreadPoolExecutor
import grpc

from server.proto import chat_pb2_grpc as rpc
from server.server import Server

ADDRESS = "localhost"
PORT = 11912


def serve():
    logging.basicConfig(level=logging.INFO)

    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    rpc.add_ChatServicer_to_server(Server(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()

    logging.info("Listening")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
