from errors.errors import TooManyUsersError
import server.proto.chat_pb2 as chat
import server.proto.chat_pb2_grpc as rpc

class Connection:
    def __init__(self):
        self.users = []
        self.chats = []

    @property
    def is_connected(self) -> bool:
        return len(self.users) == 2

    def add_user(self, user: chat.ChatUser):
        if len(self.users) < 2:
            self.users.append(user)
        else:
            raise TooManyUsersError

    def add_to_chat(self, chat):
        self.chats.append(chat)

    # TODO: go over this
    def remove_user(self, user: chat.ChatUser) -> bool:
        for existing_user in self.users:
            if existing_user.username == user.username:
                self.users.remove(user)
                return True
        return False
