import logging

import server.proto.chat_pb2 as chat
from server.proto.chat_pb2 import (
    ChatUser,
    ChatUserConnected,
    Empty,
    Message,
)
from server.proto.chat_pb2_grpc import ChatServicer
from errors.errors import (
    ConversationNotFoundError,
)
from connections.memory_manager import MemoryConnectionManager

logging.basicConfig()


class Server(ChatServicer):
    def __init__(self):
        self.connections = MemoryConnectionManager()

    def Connect(self, request: ChatUser, context) -> ChatUserConnected:
        user = request
        id = self.connections.get_or_create_available_connection(user)
        status = id is not None
        return ChatUserConnected(isConnected=status, conversationID=id)

    def Disconnect(self, request: ChatUser, context) -> ChatUserConnected:
        status = self.connection.remove_user(request)
        return ChatUserConnected(isConnected=not status)

    def SendMessage(self, request: Message, context) -> Empty:
        logging.info(f"User {request.senderID} has sent a message: {request.message}")
        try:
            connection = self.connections.get_connection_by_client_id(
                request.senderID, request.conversationID
            )
            connection.add_to_chat(request)
        except ConversationNotFoundError:
            logging.error(f"Could not find conversation {request.conversationID}")
        return Empty()

    def SubscribeMessages(self, request: ChatUser, context):
        client_id = request.username
        conversation_id = request.conversationID
        last_seen_message_index = 0

        logging.info(f"User {client_id} has subscribed to messages")
        connection = self.connections.get_connection_by_client_id(
            client_id, conversation_id
        )
        while True:
            while len(connection.chats) > last_seen_message_index:
                message = connection.chats[last_seen_message_index]
                last_seen_message_index += 1
                if message.senderID != client_id:
                    yield message
