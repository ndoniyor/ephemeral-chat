import logging
import grpc

import server.proto.chat_pb2 as chat
import server.proto.chat_pb2_grpc as rpc

logging.basicConfig()


class Client(rpc.ChatStub):
    def __init__(
        self,
        username: str,
        conversation_id: str = "",
        address: str = "localhost",
        port: int = 11912,
    ):
        self.user = chat.ChatUser()
        self.user.username = username
        self.user.conversationID = conversation_id
        channel = grpc.insecure_channel(
            f"{address}:{port}", options=(("grpc.enable_http_proxy", 0),)
        )
        self.stub = rpc.ChatStub(channel)

    def send_message(self):
        text_message = input(f"S[{self.user.username}]: ")
        message = chat.Message()
        message.senderID = self.user.username
        message.message = text_message
        message.conversationID = self.user.conversationID
        self.stub.SendMessage(message)

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
