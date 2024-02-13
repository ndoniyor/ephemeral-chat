import { ChatClient } from "./chat.client";
import { ChatRoomInfo, ChatUser, Empty, Message } from "./chat";
import { GrpcWebFetchTransport } from "@protobuf-ts/grpcweb-transport";

const host = "localhost:11912";

class ChatClientServicer {
	user: ChatUser;
	stub: ChatClient;
	isConnected: boolean;
	stream: any;

	constructor() {
		const transport = new GrpcWebFetchTransport({
			baseUrl: host
		});
		this.user = ChatUser.create();
		this.stub = new ChatClient(transport);
		this.isConnected = false;
		this.stream = null;
	}

	setUser(user: ChatUser) {
		this.user = user;
	}

	setConnected(isConnected: boolean, conversationID?: string) {
		this.isConnected = isConnected;
        if (conversationID) {
            this.user.conversationID = conversationID;
        }
	}

	getConnected() {
		return this.isConnected;
	}

	async connect() {
		const call = this.stub.connect(this.user);
		
		try{
			const response = await call.response;
			console.log(response);
		}
		catch(error){
			console.log(error);
		}

		// if (response.isConnected) {
		// 	this.setConnected(true, response.conversationID);
		// 	return true;
		// } else {
        //     this.setConnected(false);
		// 	return false;
		// }
	}

	async sendMessage(textMessage: string) {
		const message = Message.create();
		message.senderID = this.user.username;
		message.message = textMessage;
		message.conversationID = this.user.conversationID;
		let { response } = await this.stub.sendMessage(message);
	}

	async receiveMessages() {
        console.log('Subscribing to messages...');
        //return this.stub.subscribeMessages(this.user);
		let stream = this.stub.subscribeMessages(this.user);
        console.log('Subscribed');
		for await (let message of stream.responses) {
			console.log(message);
		}
	}
}

export default ChatClientServicer;
