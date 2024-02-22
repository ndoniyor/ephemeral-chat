import { GrpcWebFetchTransport } from "@protobuf-ts/grpcweb-transport";

import { ChatClient } from "./protos/chat.client";
import { ChatRoomInfo, ChatUser, Empty, Message } from "./protos/chat";


class ChatClientServicer {
	user: ChatUser;
	stub: ChatClient;
	isConnected: boolean;
	messageHistory: Array<Message>;

	constructor() {
		const host = import.meta.env.VITE_DEV_HOST_URL
		const transport = new GrpcWebFetchTransport({
			baseUrl: host,
		});

		this.user = ChatUser.create();
		this.stub = new ChatClient(transport);
		this.isConnected = false;
		this.messageHistory = [];
	}

	setUser(username: string) {
		const user = ChatUser.create({ username });
		this.user = user;
	}

	setConnected(isConnected: boolean, conversationID: string = "") {
		this.isConnected = isConnected;
        if (conversationID) {
            this.user.conversationID = conversationID;
        }
	}

	async connect() {
		const call = this.stub.connect(this.user);

		const response = await call.response;
		console.log("got response message: ", response)
		
		const status = await call.status;

		if (response.isConnected) {
			this.setConnected(true, response.conversationID);
			return [true, response.conversationID];
		} else {
            this.setConnected(false);
			return [false, response.conversationID];
		}
	}

	async sendMessage(textMessage: string) {
		const message = Message.create({
			senderID: this.user.username,
			message: textMessage,
			conversationID: this.user.conversationID,
		});
		const call = this.stub.sendMessage(message);
		const status =  await call.status;
		return status.code === "OK";
	}

	receiveMessages() {
        console.log('Subscribing to messages...');
		const call  = this.stub.subscribeMessages(this.user);
		return call.responses;
	}

	async disconnect() {
		const call = this.stub.disconnect(this.user);
		const response = await call.response;
		const status = await call.status;
		if (!response.isConnected) {
			this.setConnected(false);
			return true;
		} else {
			return false;
		}
	}

	async flushServer() {
		const call = this.stub.flushServer(Empty.create());
		const response = await call.response;
		const status = await call.status;
		console.log(response);
	}
}

export default ChatClientServicer;
