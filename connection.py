import exchange_pb2 as chat
import exchange_pb2_grpc as rpc
from client import Client


class Connection:
    def __init__(self, client1: Client, client2: Client):
        self.client1 = client1
        self.client2 = client2

    
