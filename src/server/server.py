from concurrent import futures
from collections import defaultdict
from typing import Generator, Tuple
import logging
from uuid import uuid4

import grpc
import server.proto.chat_pb2 as chat
from server.proto.chat_pb2 import (
    ChatUser,
    ChatUserConnected,
    Empty,
    Message,
)
from server.proto.chat_pb2_grpc import ChatServicer
from errors.errors import TooManyUsersError
from server.connection import Connection


class Server(ChatServicer):
    def __init__(self):
        self.connections = {}

    # TODO: Directly add connection to available connections list
    def _create_connection(self, user: ChatUser) -> str:
        connection = Connection()
        connection.add_user(user)
        id = str(uuid4())
        self.connections[id] = connection
        return id

    # TODO: Maintain list of available connections to reduce time complexity of search
    def _get_or_create_available_connection(self, user: ChatUser) -> str | None:
        for id, connection in self.connections.items():
            if len(self.connections[connection].users) < 2:
                return id
        try:
            return self._create_connection(user)
        except TooManyUsersError:
            return None
        
    def _get_connection_by_sender_id(self, sender_id: str) -> Connection:
        for connection in self.connections.values():
            for user in connection.users:
                if user.username == sender_id:
                    return connection
        raise ValueError(f"User {sender_id} not found")

    def Connect(self, request: ChatUser, context) -> ChatUserConnected:
        user = request
        id = self._get_or_create_available_connection(user)
        status = id is not None
        return ChatUserConnected(isConnected=status, conversationID=id)

    def Disconnect(self, request: ChatUser, context) -> ChatUserConnected:
        status = self.connection.remove_user(request)
        return ChatUserConnected(isConnected=not status)

    def SendMessage(self, request: Message, context) -> Empty:
        logging.info(f"User {request.senderID} has sent a message: {request.message}")
        connection = _get_connection_by_sender_id(request.senderID)
        tion.add_to_chat(request)
        return Empty()

    def SubscribeMessages(self, request: ChatUser, context):
        client_id = request.username
        last_seen_message_index = 0

        logging.info(f"User {client_id} has subscribed to messages")
        while True:
            while len(self.connection.chats) > last_seen_message_index:
                message = self.connection.chats[last_seen_message_index]
                last_seen_message_index += 1
                if message.senderID != client_id:
                    yield message
