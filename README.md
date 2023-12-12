# Ephemeral Chat

This is a simple chat server implemented in Python using gRPC. Functionality will be extended periodically. My end goal for this is a service that:
* Allows two users to talk to each other
* Encrypted via TLS
* Conversations can be cached for a limited time or completely ephemeral, deleting after both users disconnect

## Features

- Connect and disconnect users
- Send and receive messages in real-time


## To-Do
- [ ] Allow for multiple connections and keep them all separate (*in-progress*)
- [ ] Serve gRPC server via Django
- [ ] Add encryption to protect messages as they're transported
- [ ] Add cache DB to allow users to persist conversations for set time


## Dependencies

- Python 3.7+
- gRPC
- ProtoBuf

## Usage

1. Clone the repository:

```sh
$ git clone https://github.com/ndoniyor/ephemeral-chat
```

2. Navigate to the project directory:

```sh
$ cd ephemeral-chat
```

3. Install the required dependencies:

```sh
$ conda env create -f environment.yml
```

4. Run the server:

```sh
$ python src/server/server.py
```

The server will start listening for connections on `localhost:11912`.

5. Run the client(s):

```sh
$ python src/client/client.py
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