import { useState, useEffect } from "react";
import ChatClientServicer from "./chat/chatClientServicer";
import { Message } from "./chat/protos/chat";
import MessageBox from "./components/MessageBox";

// need to move this to inside app after local storage serialization is set up
// then deserialize and reconstruct with useeffect
const chatClient = new ChatClientServicer();

function App() {
	const [connectionStatus, setConnectionStatus] = useState(false);
	const [conversationID, setConversationID] = useState("");
	const [username, setUsername] = useState("");
	const [messageToSend, setMessageToSend] = useState("");
	const [messageHistory, setMessages] = useState<Message[]>([]);

	useEffect(() => {
		if (connectionStatus) {
			let chatStream = chatClient.receiveMessages();
			chatStream.onMessage((message) => {
				setMessages((prevMessages) => [...prevMessages, message]);
			});
		}
	}, [connectionStatus, chatClient]);

	const handleConnect = async () => {
		chatClient.setUser(username);
		const [status, id] = await chatClient.connect();
		setConnectionStatus(status as boolean);
		setConversationID(id as string);
	};

	const handleSendMessage = async () => {
		const success = await chatClient.sendMessage(messageToSend);
		if (success) {
			const message = Message.create({
				senderID: username,
				message: messageToSend,
			});
			setMessages((prevMessages) => [...prevMessages, message]);
		}
	};

	const handleFlush = async () => {
		await chatClient.flushServer();
	};

	return (
		<div className="flex-col justify-center">
			<button onClick={handleFlush}>Flush</button>
			<div>
				{connectionStatus ? (
					<div>
						<h2>You are connected to: {conversationID}</h2>
						<h3>Username: {username}</h3>
					</div>
				) : (
					<h2>You are not connected</h2>
				)}
			</div>
			<div>
				{!connectionStatus ? (
					<div>
						<label htmlFor="username-field">Name:</label>
						<input
							id="username-field"
							onChange={(e) => {
								setUsername(e.target.value);
							}}
						/>
						<button onClick={handleConnect}>Enter</button>
					</div>
				) : (
					<div>
						<MessageBox
							user={chatClient.user}
							messageList={messageHistory}
						/>
						<label htmlFor="message-field">[{username}]: </label>
						<input
							id="message-field"
							onChange={(e) => {
								setMessageToSend(e.target.value);
							}}
						/>
						<button onClick={handleSendMessage}>Send</button>
					</div>
				)}
			</div>
		</div>
	);
}

export default App;
