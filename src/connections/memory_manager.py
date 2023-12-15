import logging
from uuid import uuid4
from connections.connection_manager import ConnectionManager
from errors.errors import ConversationNotFoundError, TooManyUsersError
from server.connection import Connection
from server.proto.chat_pb2 import ChatUser


class MemoryConnectionManager(ConnectionManager):
    # TODO: Directly add connection to available connections list
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

    def get_or_create_available_connection_id(self, user: ChatUser) -> str | None:
        if len(self.available_connections) > 0:
            """
            So issue right now is I can either add conversations with O(1) with append,
            and then remove with pop(0) which is O(n)

            Or I can add conversations with O(n) with insert(0)
            and then remove with pop(-1) which is O(1)

            Could also look into queues
            """
            connection = self.available_connections[-1]
            connection.add_user(user)
            if connection.is_full:
                self.connections[
                    connection.conversation_id
                ] = self.available_connections.pop()
            return connection.conversation_id
        try:
            new_connection = self._create_connection(user)
            return new_connection.conversation_id

        except TooManyUsersError:
            return None

    def get_connection_by_conversation_id(
        self, conversation_id: str
    ) -> Connection:
        logging.info(f"Looking for conversation: {conversation_id}")
        try:
            return self.connections[conversation_id]
        except KeyError:
            raise ConversationNotFoundError
