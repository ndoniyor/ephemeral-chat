import logging
from typing import Iterator

import servicer.chat_pb2 as chat
from servicer.chat_pb2 import (
    ChatUser,
    ChatRoomInfo,
    Empty,
    Message,
)
from servicer.chat_pb2_grpc import ChatServicer
from errors.errors import (
    ConversationNotFoundError,
)
from connections.memory_manager import MemoryConnectionManager

CHAT_LIMIT_DEFAULT = 2


class Server(ChatServicer):
    def __init__(self):
        self.connections = MemoryConnectionManager()

    def _construct_kill_message(self, conversation_id: str) -> Message:
        message = Message()
        message.senderID = "Server"
        message.message = "kill connection"
        message.conversationID = conversation_id
        return message

    def Connect(self, request: ChatUser, context) -> ChatRoomInfo:
        user = request
        conversation_id = self.connections.get_or_create_available_connection_id(user)
        status = conversation_id is not None
        if status:
            logging.info(
                f"User {user.username} has successfully connected to {conversation_id}"
            )
        return ChatRoomInfo(
            isConnected=status,
            conversationID=conversation_id,
            userLimit=CHAT_LIMIT_DEFAULT,
        )

    def Disconnect(self, request: ChatUser, context) -> ChatRoomInfo:
        user_id = request.username
        conversation_id = request.conversationID
        connection = self.connections.get_connection_by_conversation_id(conversation_id)
        # returns true if user was removed
        connection.deactivate()
        logging.info(f"User {user_id} has successfully disconnected")
        connection.is_active = False
        return ChatRoomInfo(isConnected=False)

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

    def SubscribeMessages(self, request: ChatUser, context) -> Iterator[Message]:
        client_id = request.username
        conversation_id = request.conversationID
        last_seen_message_index = 0

        connection = self.connections.get_connection_by_conversation_id(conversation_id)
        logging.info(f"User {client_id} has subscribed to messages")

        if not connection.is_active:
            yield self._construct_kill_message(conversation_id)
        while connection.is_active:
            while len(connection.chats) > last_seen_message_index:
                message = connection.chats[last_seen_message_index]
                last_seen_message_index += 1
                if message.senderID != client_id:
                    yield message
