from concurrent import futures
from collections import defaultdict
from typing import Generator
import logging

import grpc
import server.proto.chat_pb2 as chat
import server.proto.chat_pb2_grpc as rpc
from server.connection import Connection


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
        logging.info(f"User {request.senderID} has sent a message: {request.message}")
        self.connection.add_to_chat(request)
        return chat.Empty()

    def SubscribeMessages(
        self, request: chat.ChatUser, context
    ):
        client_id = request.username
        last_seen_message_index = 0

        logging.info(f"User {client_id} has subscribed to messages")
        while True:
            while len(self.connection.chats) > last_seen_message_index:
                message = self.connection.chats[last_seen_message_index]
                last_seen_message_index += 1
                if message.senderID != client_id:
                    yield message
