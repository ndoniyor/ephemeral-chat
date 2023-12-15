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
        self.available_connections = []

    def _create_connection(self, user: ChatUser) -> str:
        connection = Connection()
        connection.add_user(user)
        id = str(uuid4())
        self.available_connections.append(id)
        self.connections[id] = connection
        return id

    def get_or_create_available_connection(self, user: ChatUser) -> str | None:
        if len(self.available_connections) > 0:
            # TODO: Modify this so that conversations waiting the longest are prioritized
            '''
            So issue right now is I can either add conversations with O(1) with append, 
            and then remove with pop(0) which is O(n)
            
            Or I can add conversations with O(n) with insert(0)
            and then remove with pop(-1) which is O(1)
            
            Could also look into queues
            '''
            return self.available_connections.pop()
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
