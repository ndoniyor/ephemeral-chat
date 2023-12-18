from errors.errors import TooManyUsersError
import server.proto.chat_pb2 as chat
import server.proto.chat_pb2_grpc as rpc

CHAT_LIMIT_DEFAULT = 2


class Connection:
    def __init__(self, conversation_id: str, user_limit: int = CHAT_LIMIT_DEFAULT):
        self.users = []
        self.chats = []
        self.conversation_id = conversation_id
        self.user_limit = user_limit
        self.is_active = False

    @property
    def is_full(self) -> bool:
        return len(self.users) >= self.user_limit

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def add_user(self, user: chat.ChatUser):
        if len(self.users) < self.user_limit:
            self.users.append(user)
        else:
            raise TooManyUsersError

    def add_to_chat(self, chat):
        self.chats.append(chat)

    # TODO: go over this
    def disconnect_user(self, user: chat.ChatUser) -> bool:
        for existing_user in self.users:
            if existing_user.username == user.username:
                self.users.remove(existing_user)
                return True
        return False
