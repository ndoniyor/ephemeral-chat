import { useState } from "react";
import ChatClientServicer from "./chat/chatClientServicer";
import { Message } from "./chat/protos/chat";
import MessageBox from "./components/MessageBox";
import UserCreationForm from "./components/UserCreationForm";
import { ChatClientProvider } from "./context/ChatClientContext";
import ConnectionStatusBanner from "./components/ConnectionStatusBanner";
import SendMessageBox from "./components/SendMessageBox";

// need to move this to inside app after local storage serialization is set up
// then deserialize and reconstruct with useeffect
const chatClient = new ChatClientServicer();

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
