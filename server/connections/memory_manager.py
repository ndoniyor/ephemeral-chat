import logging
from uuid import uuid4
from connections.connection_manager import ConnectionManager
from errors.errors import ConversationNotFoundError, TooManyUsersError
from servicer.connection import Connection
from servicer.protos.chat_pb2 import ChatUser


class MemoryConnectionManager(ConnectionManager):
    def __init__(self):
        self.connections = {}
        self.available_connections = []

    def _create_connection(self, user: ChatUser) -> Connection:
        id = str(uuid4())
        new_connection = Connection(conversation_id=id)
        new_connection.add_user(user)

        self.connections[id] = new_connection
        self.available_connections.insert(0, new_connection)

        return new_connection

    def get_or_create_available_connection_id(self, user: ChatUser) -> str:
        logging.info(f"Looking to match User {user.username}")
        if len(self.available_connections) > 0:
            connection = self.available_connections[-1]
            connection.add_user(user)
            if connection.is_full:
                self.connections[
                    connection.conversation_id
                ] = self.available_connections.pop()
            return connection.conversation_id
        try:
            logging.info("No available connections, creating new one")
            new_connection = self._create_connection(user)
            new_connection.activate()
            return new_connection.conversation_id

        except TooManyUsersError:
            return None

    def get_connection_by_conversation_id(self, conversation_id: str) -> str:
        try:
            return self.connections[conversation_id]
        except KeyError:
            raise ConversationNotFoundError
