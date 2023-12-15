import logging
import grpc

from server.proto.chat_pb2 import Empty, Message, ChatUser
import server.proto.chat_pb2_grpc as rpc


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

    def send_message(self) -> Empty | bool:
        try:
            text_message = input(f"S[{self.user.username}]: ")
            message = Message()
            message.senderID = self.user.username
            message.message = text_message
            message.conversationID = self.user.conversationID
            self.stub.SendMessage(message)
        except KeyboardInterrupt:
            return self.disconnect_from_server()

    def receive_messages(self):
        response = self.subscribe_messages()
        for res in response:
            print(
                f"\nR[{res.senderID}]: {res.message}\nS[{self.user.username}]: ", end=""
            )

    def connect_to_server(self):
        logging.info("Connecting to server...")
        response = self.stub.Connect(self.user)
        if response.isConnected:
            logging.info(f"Connected to conversation {response.conversationID}")
            self.user.conversationID = response.conversationID
        return response.isConnected

    def disconnect_from_server(self):
        response = self.stub.Disconnect(self.user)
        return response

    def subscribe_messages(self):
        return self.stub.SubscribeMessages(self.user)
