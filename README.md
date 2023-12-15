# Ephemeral Chat

This is a simple chat server implemented in Python using gRPC. Functionality will be extended periodically. My end goal for this is a service that:

- Allows users to talk to each other
- Encrypted via TLS
- Conversations can be cached for a limited time or completely ephemeral--deleting after both users disconnect

## Features

- Connect and disconnect users
- Send and receive messages in real-time
- Supports multiple separate conversations

## To-Do

- [x] Allow for multiple connections and keep them all separate
- [ ] Add option to set user limit for chat rooms
- [ ] Figure out storage for conversations (keep them non-persistent)
- [ ] Serve gRPC server via Django
- [ ] Add encryption to protect messages as they're transported

## Dependencies

- Python 3.7+
- gRPC
- ProtoBuf

## Usage

1. Clone the repository:

    ```sh
    git clone https://github.com/ndoniyor/ephemeral-chat
    ```

2. Navigate to the project directory:

    ```sh
    cd ephemeral-chat
    ```

3. Install the required dependencies:

    ```sh
    conda env create -f environment.yml
    ```

4. Run the server:

    ```sh
    python src/serve.py
    ```

    The server will start listening for connections on `localhost:11912`.

5. Run the client(s):

    ```sh
    python src/connect.py
    ```

## API

The server provides the following gRPC methods:

- `Connect(ChatUser) -> ChatUserConnected`: Connect a user to the chat server.
- `Disconnect(ChatUser) -> ChatUserConnected`: Disconnect a user from the chat server.
- `SendMessage(Message) -> Empty`: Sends a message to the server
- `SubscribeMessages(ChatUser) -> stream Message`: Subscribe a user to receive messages.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
