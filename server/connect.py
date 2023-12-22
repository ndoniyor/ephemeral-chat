import logging
from random import randint
from threading import Thread

from servicer.user import User
from test_client.client import Client

ADDRESS = "localhost"
PORT = 11912


def setup_cli(client):
    message_queue_thread = Thread(target=client.receive_messages)
    message_queue_thread.start()
    while True:
        response = client.send_message()
        if response == False:
            break


if __name__ == "__main__":
    username = "Client" + str(randint(0, 100))
    c = Client(username)
    if not c.connect_to_server():
        raise Exception
    logging.info("Client has connected to server")
    setup_cli(c)
