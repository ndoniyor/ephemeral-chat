from concurrent import futures
from collections import defaultdict
import time

import grpc
import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

from connection import Connection

ADDRESS = "localhost"
PORT = 11912


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_ChatServerServicer_to_server(Server(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    server.wait_for_termination()


class Server(rpc.ChatServerServicer):
    def __init__(self):
        # self.connection = Connection()
        self.connections = defaultdict(list)

    # def create_connection(self, client1, client2):
    #     self.connection.client1, self.connection.client2 = client1, client2

    def ChatStream(self, request_iterator, context):
        client_id = context.peer()
        self.connections[client_id] = context
        for new_message in request_iterator:
            for prev_note in self.connections[client_id]["chat"]:
                if prev_note.location == new_message.location:
                    yield prev_note
            self.chats.append(new_message).append(new_message)

    def SendMessage(self, request: chat.Message, context):
        sender_id = context.peer()
        receiver_id = request.receiver_id
        message = request.message
        print(f"From [{sender_id}] to [{receiver_id}]: {message}")
        return chat.Empty()


if __name__ == "__main__":
    serve()
