import dotenv from "dotenv";

import { GrpcWebFetchTransport } from "@protobuf-ts/grpcweb-transport";

import { ChatClient } from "./chat.client";
import { ChatRoomInfo, ChatUser, Empty, Message } from "./chat";


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

	setUser(user: ChatUser) {
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
			return true;
		} else {
            this.setConnected(false);
			return false;
		}
	}

	async sendMessage(textMessage: string) {
		const message = Message.create({
			senderID: this.user.username,
			message: textMessage,
			conversationID: this.user.conversationID,
		});
		const call = this.stub.sendMessage(message);
		const response =  await call.response;
		console.log(response);
	}

	async receiveMessages() {
        console.log('Subscribing to messages...');
        
		let stream = this.stub.subscribeMessages(this.user);
        console.log('Subscribed');
		for await (let message of stream.responses) {
			this.messageHistory.push(message);
		
		}
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
}

export default ChatClientServicer;
