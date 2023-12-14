import logging
from random import randint

from server.user import User
from client.client import Client

ADDRESS = "localhost"
PORT = 11912

if __name__ == "__main__":
    logging.basicConfig()
    username = "Client" + str(randint(0, 100))
    c = Client(username)
    if not c.connect_to_server():
        raise Exception
    c.setup_cli()
