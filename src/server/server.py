from concurrent import futures
from collections import defaultdict
from typing import Generator
import logging

import grpc
import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

from connection import Connection
from src.utils.helpers import log_args

ADDRESS = "localhost"
PORT = 11912


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_ChatServicer_to_server(Server(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    print("Listening")
    server.wait_for_termination()


class Server(rpc.ChatServicer):
    def __init__(self):
        self.connections = defaultdict(Connection)

    def Connect(self, request: chat.ChatUser, context) -> chat.ChatUserConnected:
        status = self.connection.add_user(request)
        if status:
            logging.info(f"User {request.username} has connected")
        return chat.ChatUserConnected(isConnected=status)

    def Disconnect(self, request, context) -> chat.ChatUserConnected:
        status = self.connection.remove_user(request)
        return chat.ChatUserConnected(isConnected=not status)

    def SendMessage(self, request: chat.Message, context) -> chat.Empty:
        logging.info(f"User {request.senderID} has sent a message")
        message = request.message
        self.connection.add_to_chat(request)
        print(message)
        return chat.Empty()

    # rpc SubscribeMessages(stream Message) returns (stream Message)
    def SubscribeMessages(self, request: chat.ChatUser, context) -> Generator[chat.Message]:
        client_id = request.username
        last_seen_message_index = 0

        logging.info(f"User {client_id} has subscribed to messages")
        while True:
            while len(self.connection.chats) > last_seen_message_index:
                message = self.connection.chats[last_seen_message_index]
                last_seen_message_index += 1
                if message.senderID != client_id:
                    yield message


if __name__ == "__main__":
    logging.basicConfig()
    serve()
