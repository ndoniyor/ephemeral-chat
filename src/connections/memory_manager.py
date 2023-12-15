import logging
from uuid import uuid4
from connections.connection_manager import ConnectionManager
from errors.errors import ConversationNotFoundError, TooManyUsersError
from server.connection import Connection
from server.proto.chat_pb2 import ChatUser

logging.basicConfig()


class MemoryConnectionManager(ConnectionManager):
    # TODO: Directly add connection to available connections list
    def __init__(self):
        self.connections = {}

    def _create_connection(self, user: ChatUser) -> str:
        connection = Connection()
        connection.add_user(user)
        id = str(uuid4())
        self.connections[id] = connection
        return id

    # TODO: Maintain list of available connections to reduce time complexity of search
    def get_or_create_available_connection(self, user: ChatUser) -> str | None:
        for id in self.connections.keys():
            connection = self.connections[id]
            if len(connection.users) < 2:
                connection.add_user(user)
                return id
        try:
            return self._create_connection(user)
        except TooManyUsersError:
            return None

    def get_connection_by_client_id(
        self, sender_id: str, conversation_id: str
    ) -> Connection:
        logging.info(f"Looking for conversation: {conversation_id}")
        try:
            return self.connections[conversation_id]
        except KeyError:
            raise ConversationNotFoundError
