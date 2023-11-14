import threading

import grpc
import chat_pb2 as chat
import chat_pb2_grpc as rpc

ADDRESS = 'localhost'
PORT = 11912

class Client:
    def __init__(self, username: str,):
        self.username = username

        channel = grpc.insecure_channel(f"{ADDRESS}:{PORT}")
        self.stub = rpc.ChatServerStub(channel)
        threading.Thread(target=self._listen_for_messages, daemon=True).start()
    
    def _listen_for_messages(self):
        for note in self.stub.ChatStream(chat.Empty()):
            print(f"R[{note.sender_id}] {note.message}")
            self.chat_list.append(f"[{note.sender_id}] {note.message}\n")

    def send_message(self, message):
        if message:
            note = chat.Message()
            note.sender_id = self.username
            note.message = message
            print(f"S[{note.sender_id}] {note.message}")
            self.stub.SendMessage(note)

    def setup_cli(self):
            print("Enter 'exit' to quit")
            while True:
                message = input("Enter message: ")
                if message.lower() == 'exit':
                    break
                self.send_message(message)


if __name__ == '__main__':
    username = "Client" 
    c = Client(username)
    c.setup_cli()