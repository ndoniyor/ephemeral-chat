import logging

import server.proto.chat_pb2 as chat
from server.proto.chat_pb2 import (
    ChatUser,
    ChatRoomInfo,
    Empty,
    Message,
)
from server.proto.chat_pb2_grpc import ChatServicer
from errors.errors import (
    ConversationNotFoundError,
)
from connections.memory_manager import MemoryConnectionManager

CHAT_LIMIT_DEFAULT = 3


class Server(ChatServicer):
    def __init__(self):
        self.connections = MemoryConnectionManager()

    def Connect(self, request: ChatUser, context) -> ChatRoomInfo:
        user = request
        id = self.connections.get_or_create_available_connection_id(user)
        status = id is not None
        return ChatRoomInfo(
            isConnected=status, conversationID=id, userLimit=CHAT_LIMIT_DEFAULT
        )

    def Disconnect(self, request: ChatUser, context) -> ChatRoomInfo:
        user_id = request.username
        conversation_id = request.conversationID
        connection = self.connections.get_connection_by_conversation_id(conversation_id)
        status = connection.remove_user(request)
        if status:
            logging.info(f"User {user_id} has successfully disconnected")
        return ChatRoomInfo(isConnected=not status)

    def SendMessage(self, request: Message, context) -> Empty:
        logging.info(f"User {request.senderID} has sent a message: {request.message}")
        try:
            connection = self.connections.get_connection_by_conversation_id(
                request.conversationID
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
        connection = self.connections.get_connection_by_conversation_id(conversation_id)
        # TODO make this run until connection closed
        while True:
            while len(connection.chats) > last_seen_message_index:
                message = connection.chats[last_seen_message_index]
                last_seen_message_index += 1
                if message.senderID != client_id:
                    yield message
