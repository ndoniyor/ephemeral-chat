import { useState } from "react";
import ChatServiceClientHandler from "./chatServiceClient/chatServiceClientHandler";
import { Message } from "./chatServiceClient/generatedProtos/chat_service";
import MessageBox from "./components/MessageBox";
import UserCreationForm from "./components/UserCreationForm";
import { ChatClientProvider } from "./context/ChatClientContext";
import ConnectionStatusBanner from "./components/ConnectionStatusBanner";
import SendMessageBox from "./components/SendMessageBox";

// need to move this to inside app after local storage serialization is set up
// then deserialize and reconstruct with useeffect
const chatClient = new ChatServiceClientHandler();

function App() {
	const [connectionStatus, setConnectionStatus] = useState(false);
	const [conversationID, setConversationID] = useState("");
	const [messageHistory, setMessages] = useState<Message[]>([]);

	const handleFlush = async () => {
		await chatClient.flushServer();
	};

	return (
		<ChatClientProvider client={chatClient}>
			<div className="flex-col justify-center">
				<button className="btn-neutral" onClick={handleFlush}>
					Flush
				</button>
				<div>
					<ConnectionStatusBanner
						connectionStatus={connectionStatus}
						conversationID={conversationID}
					/>
				</div>
				<div>
					{!connectionStatus ? (
						<UserCreationForm
							setConnectionStatus={setConnectionStatus}
							setConversationID={setConversationID}
							setMessages={setMessages}
						/>
					) : (
						<div>	
							<MessageBox
								user={chatClient.user}
								messageList={messageHistory}
							/>
							<SendMessageBox setMessages={setMessages} />
						</div>
					)}
				</div>
			</div>
		</ChatClientProvider>
	);
}

export default App;
