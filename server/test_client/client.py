import grpc

from servicer.protos.chat_pb2 import Empty, Message, ChatUser
import servicer.protos.chat_pb2_grpc as rpc


class Client(rpc.ChatStub):
    def __init__(
        self,
        username: str,
        conversation_id: str = "",
        address: str = "localhost",
        port: int = 11912,
    ):
        self.user = ChatUser()
        self.user.username = username
        self.user.conversationID = conversation_id
        channel = grpc.insecure_channel(
            f"{address}:{port}", options=(("grpc.enable_http_proxy", 0),)
        )
        self.stub = rpc.ChatStub(channel)
        self.is_connected = False

    def send_message(self) -> Empty | bool:
        text_message = input(f"S[{self.user.username}]: ")
        if text_message == "/exit":
            if not self.disconnect_from_server():
                self.is_connected = False
                return False
        message = Message()
        message.senderID = self.user.username
        message.message = text_message
        message.conversationID = self.user.conversationID
        self.stub.SendMessage(message)

    def receive_messages(self):
        while self.is_connected == True:
            response = self.stub.SubscribeMessages(self.user)

            for res in response:
                if res.message == "kill connection" and res.senderID == "Server":
                    status = self.disconnect_from_server()
                    if not status:
                        self.is_connected = False
                        return
                print(
                    f"\nR[{res.senderID}]: {res.message}\nS[{self.user.username}]: ",
                    end="",
                )

    def connect_to_server(self):
        response = self.stub.Connect(self.user)
        if response.isConnected:
            self.user.conversationID = response.conversationID
            self.is_connected = True
        return response.isConnected

    def disconnect_from_server(self):
        response = self.stub.Disconnect(self.user)
        if response.isConnected == False:
            self.connected = False
        return response.isConnected
