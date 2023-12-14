import server.proto.chat_pb2 as chat
import server.proto.chat_pb2_grpc as rpc

from server.user import User


class Connection:
    def __init__(self):
        self.user1 = None
        self.user2 = None
        self.chats = []

    @property
    def is_connected(self) -> bool:
        return self.user1 and self.user2

    def add_user(self, user: chat.ChatUser) -> bool:
        try:
            if not self.user1:
                self.user1 = user
            elif not self.user2:
                self.user2 = user
            return True
        except Exception:
            return False

    def add_to_chat(self, chat):
        self.chats.append(chat)
    
    def remove_user(self, user: chat.ChatUser) -> bool:
        try:
            if self.user1 == user:
                self.user1 = None
            elif self.user2 == user:
                self.user2 = None
            return True
        except Exception:
            return False
