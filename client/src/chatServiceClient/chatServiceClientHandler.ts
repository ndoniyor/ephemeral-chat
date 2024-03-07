import { GrpcWebFetchTransport } from "@protobuf-ts/grpcweb-transport";
import type { RpcOutputStream } from "@protobuf-ts/runtime-rpc";

import { ChatServiceClient } from './generatedProtos/chat_service.client';

import { ChatUser, Empty, Message } from "./generatedProtos/chat_service";

interface ConnectionResponse {
	status: boolean;
	conversationID: string;
	stream: RpcOutputStream<Message> | null;
}


class ChatServiceClientHandler {
	user: ChatUser;
	stub: ChatServiceClient;
	isConnected: boolean;
	messageHistory: Array<Message>;

	constructor() {
		const host = import.meta.env.VITE_DEV_HOST_URL
		const transport = new GrpcWebFetchTransport({
			baseUrl: host,
		});

		this.user = ChatUser.create();
		this.stub = new ChatServiceClient(transport);
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

	async connect(): Promise<ConnectionResponse> {
		const call = this.stub.connect(this.user);

		const response = await call.response;
		console.log("got response message: ", response)

		if (response.isConnected) {
			this.setConnected(true, response.conversationID);
			const stream = this.receiveMessages();
			return { status: true, conversationID: response.conversationID, stream };
		} else {
            this.setConnected(false);
			return { status: false, conversationID: "", stream: null };
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
		console.log(response);
	}
}

export default ChatServiceClientHandler;
