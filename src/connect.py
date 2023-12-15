import logging
from random import randint
from threading import Thread

from server.user import User
from client.client import Client

ADDRESS = "localhost"
PORT = 11912

def setup_cli(client):
    Thread(target=client.receive_messages).start()
    while True:
        client.send_message()
            
if __name__ == "__main__":
    logging.basicConfig()
    username = "Client" + str(randint(0, 100))
    c = Client(username)
    if not c.connect_to_server():
        raise Exception
    logging.info("Client has connected to server")
    setup_cli(c)
