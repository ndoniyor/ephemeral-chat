import logging
from uuid import uuid4
from connection_manager import ConnectionManager
from errors.errors import ConversationNotFoundError, TooManyUsersError
from server.connection import Connection
from server.proto.chat_pb2 import ChatUser

logging.basicConfig()


class MemoryConnectionManager(ConnectionManager):
    # TODO: Directly add connection to available connections list
    @classmethod
    def _create_connection(cls, user: ChatUser) -> str:
        connection = Connection()
        connection.add_user(user)
        id = str(uuid4())
        cls.connections[id] = connection
        return id

    # TODO: Maintain list of available connections to reduce time complexity of search
    @classmethod
    def _get_or_create_available_connection(cls, user: ChatUser) -> str | None:
        for id in cls.connections.keys():
            connection = cls.connections[id]
            if len(connection.users) < 2:
                connection.add_user(user)
                return id
        try:
            return cls._create_connection(user)
        except TooManyUsersError:
            return None

    @classmethod
    def _get_connection_by_client_id(
        cls, sender_id: str, conversation_id: str
    ) -> Connection:
        logging.info(f"Looking for conversation: {conversation_id}")
        try:
            return cls.connections[conversation_id]
        except KeyError:
            raise ConversationNotFoundError
